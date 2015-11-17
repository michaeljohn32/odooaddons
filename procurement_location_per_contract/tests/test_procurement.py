# -*- coding: utf-8 -*-
# © 2015 John Walsh michaeljohn32@yahoo.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp.tests.common import TransactionCase
class TestContractToProcurement(TransactionCase):
    def test_creations(self):
        self.sales_order_id.action_button_confirm()
        procurements = self.env['procurement.order'].search([('group_id.name','=',self.sales_order_id.name),('state','=','confirmed')])
        for p in procurements:
            p.run()
        location = self.env['stock.location'].search([('project_id','=',self.project_id.id)])
        rule = self.env['procurement.rule'].search([('project_id','=',self.project_id.id)])
        self.assertNotEqual(location.id, False,msg="Expected a location associated with contract to be created, no location found")
        self.assertNotEqual(rule.id, False,msg="Expected a procurement rule associated with contract to be created, no rule found")
    def test_proc_locations(self):
        self.sales_order_id.action_button_confirm()
        procurements = self.env['procurement.order'].search([('group_id.name','=',self.sales_order_id.name),('state','=','confirmed')])
        for p in procurements:
            p.run()
        location = self.env['stock.location'].search([('project_id','=',self.project_id.id)])
        procurements = self.env['procurement.order'].search([('group_id.name','=',self.sales_order_id.name),('location_id','=',location.id)])
        self.assertNotEqual(len(procurements), 0,msg="Expected at least one procurement to the newly created location, no procurement found referencing contract location")

    def setUp(self):
        super(TestContractToProcurement, self).setUp()
        self.warehouse_id = self.env.ref('stock.warehouse0')
        self.warehouse_id.mto_mts_management = True # enable mts+mto
        if(self.warehouse_id.delivery_steps != 'pick_ship'):
            self.warehouse_id.change_route(self.warehouse_id, new_delivery_step='pick_ship')
        self.product_id = self.env.ref('product.product_product_4')
        mto_mts_route = self.env.ref('stock_mts_mto_rule.route_mto_mts')
        self.product_id.route_ids = [(6, 0, [mto_mts_route.id])] # product is mts+mto route
        self.company_partner_id = self.env.ref('base.main_partner')
        self.customer_id = self.env.ref('base.res_partner_2')
        self.project_id = self.env.ref('procurement_location_per_contract.analytic_account_contract')
#        self.project_id = self.env['account.analytic.account'].create({
#            'name': 'Contract1',
#            'type': 'contract',
#        })

        sale_order_creation = {
            'partner_id': self.customer_id.id,
            'partner_invoice_id': self.customer_id.id,
            'partner_shipping_id': self.customer_id.id,
            'project_id': self.project_id.id,
            'order_line': [(0,0,{
                'product_id': self.product_id.id,
                'name': self.product_id.name,
                'price_unit': self.product_id.list_price,
                'product_uom': self.product_id.uom_id.id,
                'product_uom_qty': 300,
                'state': 'draft',
            })]
        }
        self.sales_order_id = self.env['sale.order'].create(sale_order_creation)
        self.quant = self.env['stock.quant'].create({
            'owner_id': self.company_partner_id.id,
            'location_id': self.env.ref('stock.stock_location_stock').id,
            'product_id': self.product_id.id,
            'qty': 0.0,
        })

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
