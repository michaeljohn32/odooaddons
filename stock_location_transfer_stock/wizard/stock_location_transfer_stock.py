# -*- coding: utf-8 -*-
# © 2015 John Walsh michaeljohn32@yahoo.com 
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import models, fields, api, exceptions
class StockLocationTransferStock(models.TransientModel):
    _name = 'stock.location.transfer_wiz'
    _description = 'Move All Stock In One Location To A New Location'
    dest_loc_id = fields.Many2one('stock.location', 'Destination Location', help='All selected locations will be moved to this location')

    @api.multi
    def transfer_stock(self):
        '''
        This method transfers all the locations in active ids to the destination location
        @param: self
        @return: view of the created pickings or empty tree view if none created
        '''
        locations = self.env['stock.location'].browse(self.env.context['active_ids'])
        # Sanity Check locations
        if self.dest_loc_id.id in locations.ids:
            raise exceptions.ValidationError("Location " + self.dest_loc_id.name + " cannot be one of the selected locations")
        picking_ids = []
        for location in locations:
            if(location.usage != 'internal'):
                raise exceptions.ValidationError("Location " + location.name + " must be an Internal Location")
        # If the locations have unreserved stock, make a picking per location for moving
        # this stock
        for location in locations:
            move_vals = []
            picking_vals = {
                 'location_dest_id': self.dest_loc_id.id,
                 'picking_type_id': self.env['stock.picking.type'].search([('name','=','Internal Transfers')]).id
            }
            
            quants = self.env['stock.quant'].search([('location_id','child_of',location.id),('reservation_id','=',False)])
            for quant in quants: 
                move_dict = {
                    'product_id': quant.product_id.id,
                    'name': "LOC_CHANGE / " + quant.name,
                    'product_uom': quant.product_id.uom_id.id,
                    'product_uom_qty': quant.qty,
                    'location_id': location.id,
                    'location_dest_id': self.dest_loc_id.id,
                }
                move_vals.append((0,0,move_dict))
            if len(move_vals) > 0:
                picking_vals['location_id'] = location.id
                picking_vals['move_lines'] = move_vals
                # Create and assign stock to the picking
                pick = self.env['stock.picking'].create(picking_vals)
                pick.action_confirm()
                pick.action_assign()
                picking_ids.append(pick.id)
        domain = [('id','in',picking_ids)]
        return { 'type': 'ir.actions.act_window', 'res_model': 'stock.picking', 'res_id': picking_ids, 'view_type': 'form', 'view_mode': 'tree,form', 'domain': domain}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:   
