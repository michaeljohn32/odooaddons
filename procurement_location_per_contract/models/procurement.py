# -*- coding: utf-8 -*-
# © 2015 John Walsh michaeljohn32@yahoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api
import logging
import pdb
_logger = logging.getLogger(__name__)
class ProcurementGroup(models.Model):
    _inherit = 'procurement.group'
    sales_order_id = fields.Many2one('sale.order','Sales Order', compute='_compute_sales_order')
    @api.one
    def _compute_sales_order(self):
        self.sales_order_id = self.env['sale.order'].search([('name','=',self.name or False)])
class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'
    project_id = fields.Many2one('account.analytic.account', 'Contract/Analytic', help="The analytic account related to the procurement rule")
    base_rule_id = fields.Many2one(comodel_name='procurement.rule', string='Rule Based On', help="This rule is based on another procurement rule")
    project_rule_id = fields.One2many(comodel_name='procurement.rule', inverse_name='base_rule_id', string='Projects Based on This Rule', help="This rule forms the basis for the following rules")

class ProcurementOrder(models.Model):
    _inherit = 'procurement.order'
    project_id = fields.Many2one('account.analytic.account', 'Contract/Analytic', readonly=True, states={'draft': [('readonly', False)]}, help="The analytic account related to the procurement")

    @api.model
    def _get_mts_mto_procurement(self, proc, rule, qty, uos_qty):
        '''This overridden method injects a rule to procure to a job-specific
        location instead of from stock
        @param: proc - the procurement recordset
        @param: rule - the rule that is either mto or mts
        @param: qty - the quantity
        @param: uos_qty - the unit of sale quantity
        @returns: the return value of the super() method
        '''
        sales_order = proc.group_id.sales_order_id
        warehouse_id = proc.warehouse_id 
        new_rule_id = rule
        mts = False
        mto = False
#        _logger.info("Product:" + proc.product_id.name)
#        _logger.info("LOC:" + proc.location_id.name)
#        _logger.info("rule:" + rule.name)
        job_location_id = False
        if sales_order.project_id:
            job_location_id = self._get_analytic_location(warehouse_id, sales_order.project_id)
        #MTS
        if sales_order.project_id and rule.id == warehouse_id.mts_mto_rule_id.mts_rule_id.id:
            mts=True
            if proc.location_id == warehouse_id.wh_output_stock_loc_id:
                # create a new rule with a procure method of make-to-order so that it will keep procuring to move stock from stock location->contract-location
                new_rule_id = self._get_location_rule(job_location_id, rule.location_id, rule, procure_method = 'make_to_order')
            elif proc.location_id == job_location_id:
                new_rule_id = self._get_stock_to_job_rule(warehouse_id, sales_order.project_id) 
               
        if sales_order.project_id and rule.id == warehouse_id.mts_mto_rule_id.mto_rule_id.id:
            mto=True
            if proc.location_id == warehouse_id.wh_output_stock_loc_id:
                new_rule_id = self._get_location_rule(job_location_id, rule.location_id, rule, procure_method = 'make_to_order')
            elif proc.location_id == job_location_id:
                # Don't try to Manufacture/Buy it from stock
                for route in proc.product_id.route_ids:
                    if route.name == "Buy":
                        new_rule_id = route.pull_ids[0]
                        break
                    elif route.name == "Manufacture":
                        new_rule_id = route.pull_ids[0]
                        break
        res = super(ProcurementOrder, self)._get_mts_mto_procurement(proc, new_rule_id, qty, uos_qty)
        if mts:
            # make to stock requires an extra move
            # to 
            # move existing stock to project location

            # get a route to add/use a rule to
            # go from stock to the job location

            stock_to_job_route = self._get_stock_to_job_route(warehouse_id, sales_order.project_id)
            res['route_ids'] = [(6,0,[stock_to_job_route.id])]
        return res

# the following methods were used for testing
#    @api.model
#    def create(self, vals):
#        res = super(ProcurementOrder, self).create(vals)
#        return res
#    @api.model
#    def _find_suitable_rule(self, procurement):
#        res = super(ProcurementOrder, self)._find_suitable_rule(procurement)
#        return res

# Location Info
###############
    @api.model
    def _get_analytic_location(self, warehouse_id, project_id):
        '''Gets or Creates a stock.location if needed for a particular contract/analytic
        @param: self - ProcurementOrder
        @param: warehouse_id - the recordset of the warehouse to search
        @param: project_id - the recordset of the contract/analytic
        @returns: recordset(stock.location) - if location does exist, False if not'''
        parent_location = self.env.ref('stock.stock_location_stock')
        location = self.env['stock.location'].search([('location_id','=',parent_location.id),('project_id','=',project_id.id)])
        if not location:
            # create it!
            location = self._create_analytic_location(parent_location, project_id)
        return location

    @api.model
    def _create_analytic_location(self, location_id, project_id):
        '''Creates a location for an analytic account
        @param: location_id - the parent location id (will be created under this location)
        @param: project_id - the recordset of the contract/analytic
        @returns: recordset(stock.location) - the created location'''
        vals = {
            'name': project_id.name,
            'location_id': location_id.id,
            'usage': location_id.usage,
            'project_id': project_id.id,
            'comment': 'Created for Contract:' + str(project_id.name),
        }
        res = self.env['stock.location'].create(vals)
        return res

# Procurement Rule Info
#######################
    @api.model
    def _create_location_rule(self, src_loc_id, dest_loc_id, example_rule_id, keep_route=False, procure_method=False):
        '''Method to create a rule that copies the values from an example rule
        @param: src_loc_id - The project-based location that items are sourced from
        @param: dest_loc_id - The project-based location where items are needed
        @param: example_rule_id - recordset of the rule to copy
        @param: keep_route - should we add this rule to the route?
        @param: procure_method - 'make_to_stock' or 'make_to_order' 
        @returns: recordset - created rule
        '''
        route_id = example_rule_id.route_id.id
        if keep_route == False:
            route_id = False
        vals = {
            'location_src_id': src_loc_id.id,
            'name': src_loc_id.project_id.name + ": " + example_rule_id.name,
            'project_id': src_loc_id.project_id.id, 
            'route_id': route_id,
            'base_rule_id': example_rule_id.id,
        }
        if procure_method:
            vals['procure_method'] = procure_method
        new_rule = example_rule_id.copy(default=vals)
        return new_rule

    @api.model
    def _get_location_rule(self, src_loc_id, dest_loc_id, example_rule_id, keep_route=False, procure_method=False):
        '''Method to get a correct location_rule, and may create one if it doesn't exist
        @param: src_loc_id - the project-based location that items will be sourced from/to
        @param: dest_loc_id - The project-based location where items are needed
        @param: example_rule_id - the rule that the location_rule is based on i(eg a mto, mts, or internal move)
        @param: keep_route - should we add this rule to the route?
        @returns: created or found rule'''
        res = self.env['procurement.rule'].search([('base_rule_id','=',example_rule_id.id),('location_src_id','=',src_loc_id.id),('location_id','=',dest_loc_id.id)])
        if not res:
            res = self._create_location_rule(src_loc_id, dest_loc_id, example_rule_id, keep_route=keep_route, procure_method=procure_method)
        return res

    @api.model
    def _get_stock_to_job_rule(self, warehouse_id, project_id):
        '''Method to get the correct rule
        @param: warehouse_id - the current warehouse recordset 
        @param: project_id - the job  recordset 
        @returns: correct route with rule inside it'''
        stock_route_id = self.env.ref('procurement_location_per_contract.route_project_location')
        # Ensure that there's a rule for the stock move if it doesn't exist
        rule_id = self.env['procurement.rule'].search([('route_id','=',stock_route_id.id),('project_id','=',project_id.id)])
        if not rule_id:
            rule_id = self._create_stock_to_job_rule(warehouse_id, stock_route_id, project_id)
        return rule_id 
    @api.model
    def _create_stock_to_job_rule(self, warehouse_id, stock_route_id, project_id):
        '''Method to create a special rule to pull from stock
        and add it to job-specific location 
        @param: warehouse_id - the current warehouse recordset 
        @param: stock_route_id - the route that this rule should be in
        @param: project_id - the job  recordset 
        @returns: dict - the values to insert'''
        
        location_id = self.env['stock.location'].search([('project_id','=',project_id.id)])
        vals = {
            'name': 'Stock -> ' + project_id.name,
            'action': 'move',
            'picking_type_id': warehouse_id.int_type_id.id,
            'procure_method': 'make_to_stock',
            'location_src_id': warehouse_id.lot_stock_id.id,
            'location_id': location_id.id,
            'route_id': stock_route_id.id,
            'project_id': project_id.id,
        }
        new_rule_id = self.env['procurement.rule'].create(vals)
        return new_rule_id
# Procurement Route Info
#######################
    @api.model
    def _get_stock_to_job_route(self, warehouse_id, project_id):
        '''Method to get the correct route and create the appropriate rule if it doesn't exist
        @param: warehouse_id - the current warehouse recordset 
        @param: project_id - the job  recordset 
        @returns: correct route with rule inside it'''
        stock_route_id = self.env.ref('procurement_location_per_contract.route_project_location')
        # Ensure that there's a rule for the stock move if it doesn't exist
        rule_id = self._get_stock_to_job_rule(warehouse_id, project_id) 
        return stock_route_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
