# -*- encoding: utf-8 -*-
##############################################################################
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses/.
#
##############################################################################

from openerp import models, fields, api, _
from openerp.exceptions import Warning
import pdb
import logging

class stock_move(models.Model):
    _inherit = 'stock.move'
    need_to_be_costed = fields.Boolean(default=False, string="Need to Be Costed to a Produced Product")

class stock_move_consume(models.TransientModel):
    _inherit = 'stock.move.consume'
    @api.multi
    def do_move_consume(self):
        '''This method consumes a certain number of products.
        To ensure that these are costed later, we set a boolean value
        after the stock_move has been split and reset it after we've costed it
        @params: self
        @returns: bool - result of super() call
        '''
        move_ids = self.env.context.get('active_ids', False)
        moves = self.env['stock.move'].browse(move_ids)
        if(self.product_qty <= 0):
            raise Warning("You cannot consume zero or negative products.")
        elif(self.product_qty > moves.product_qty):
            raise Warning("You cannot consume more products than scheduled. Please scrap the extra quantity or add them in the 'Produce' Window.")
        # get the reserved quants
        domain = [('reservation_id', 'in', move_ids)]
        quants = self.env['stock.quant'].search(domain)
        # create a dictionary of move_ids that give the related quants' cost and quantity
        quants_dict = {}
        if quants and quants[0]:
            for quant in quants:
                quants_dict[quant.reservation_id.id] = {'cost': quant.cost, 'qty': quant.qty}
        prices = []
        for move in moves:
            if(move.id in quants_dict) and (move.product_id.product_tmpl_id.cost_method == 'real'):
                # take the real price from the quant
                #pdb.set_trace()
                move.price_unit = quants_dict[move.id]['cost']
        #pdb.set_trace()
        # call the odoo function
        res = super(stock_move_consume, self).do_move_consume()
        # now, we mark the original moves 
        # as needing to be costed
        for move_id in moves:
            move_id.need_to_be_costed = True
        return res

class mrp_production(models.Model):
    _inherit = 'mrp.production'
    logger = logging.getLogger(__name__)

    @api.multi
    @api.depends('move_created_ids2', 'move_created_ids', 'move_lines','move_lines2')
    def _get_bom_prices(self, production, production_qty, wiz, context):
        '''get the bom prices for each of the created products
        @production: mrp.production class
        @production_qty: the quantity from production
        @wiz: the wizard for the user to consume products
        @context: the context
        @returns: dict prices'''
        # validate the wizard
        produced_qty = 0.0
        for produced_prod in production.move_created_ids2:
            produced_qty += produced_prod.product_qty
        if(wiz.product_qty <= 0):
            raise Warning("You cannot produce zero or negative products.")
        elif(produced_qty + wiz.product_qty > production.product_qty):
            raise Warning("You cannot create more products than scheduled.")
        # get the quants related to the items yet to be moved
        scheduled_raw_materials = production.move_lines.ids + production.move_lines2.ids
        domain = [('reservation_id', 'in', scheduled_raw_materials)]
        quants = self.env['stock.quant'].search(domain)

        # create a dictionary of move_ids that give the related quants' cost and quantity
        quants_dict = {}
        if quants and quants[0]:
            for quant in quants:
                quants_dict[quant.reservation_id.id] = {'cost': quant.cost, 'qty': quant.qty}
        prices = []
        # We might have consumed some parts before producing this one
        for move in production.move_lines2:
            if move.need_to_be_costed:
                # Add it to this production cost ONLY ONCE
                price = move.price_unit
                prices.append({'type': 'needed_costing', 'product_id': move.product_id.id, 'unit_cost': price, 'qty': move.product_qty})
                move.need_to_be_costed = False
        for consume in wiz.consume_lines:
            # for each consume_line, we need to get the unit cost of each product
            got_price = False
            for move in production.move_lines:
                if(consume.product_id == move.product_id):
                    # This product is scheduled
                    price = move.price_unit
                    if(move.id in quants_dict) and (move.product_id.product_tmpl_id.cost_method == 'real'):
                        # take the real price from the quant
                        price = quants_dict[move.id]['cost']
                    if(consume.product_qty == move.product_qty):
                        # No change from scheduled, so we can use the price from the stock.move
                        prices.append({'type': 'matched_scheduled', 'product_id': move.product_id, 'unit_cost': price, 'qty': move.product_qty})
                        got_price = True
                        break
                    elif consume.product_qty < move.product_qty:
                        # We consume less than scheduled, but we can use the price from the stock.move cause
                        # it will split it
                        prices.append({'type': 'matched_product', 'product_id': move.product_id, 'unit_cost': price, 'qty': consume.product_qty})
                        got_price = True
                        break
                    else:
                        # FIXME:
                        # We should get the next quant, but for now, let's match the price
                        prices.append({'type': 'matched_product', 'product_id': move.product_id, 'unit_cost': price, 'qty': consume.product_qty})
                        got_price = True
                        break
            if not got_price:
                # This product was not scheduled, but it was used.
                # FIXME: should I use standard price?
                prices.append({'type': 'unscheduled_product', 'product_id': consume.product_id.id, 'unit_cost': consume.product_id.standard_price, 'qty': consume.product_qty}) 

        final_price = 0.0
        standard_price = 0.0
        for row in prices:
            final_price += row['unit_cost'] * row['qty']
            if row['type'] != 'unscheduled_product':
                standard_price += row['unit_cost'] * row['qty']
        price_dict = {}
        price_dict['final_price'] = final_price / production_qty
        price_dict['standard_price'] = standard_price / production_qty
        self.logger.info('final_price:' + str(final_price) + ':standard_price:' + str(standard_price))
        #pdb.set_trace()
        return price_dict
    @api.model
    @api.depends('move_created_ids')
    def action_produce(self, production_id, production_qty, production_mode, wiz=False, context=None):
        production = self.browse(production_id)
        stock_quants_obj = self.env['stock.quant']
        if production_mode == 'consume_produce' or production_mode == 'consume':
            for produced_product in production.move_created_ids:
                prices = self._get_bom_prices(production, production_qty, wiz, context)
                price_unit = prices['final_price']
                # not transfering to the item below
                if(produced_product.price_unit != price_unit):
                    produced_product.price_unit = price_unit
                if(produced_product.product_id.standard_price != prices['final_price']):
                    # update the product's standard price
                    msg = "Production Cost per unit: $" + str(round(prices['final_price'],2)) 
                    #pdb.set_trace()
                    production.message_post(body=msg)
                    msg += ", set from " + str(production.name)
                    produced_product.product_id.message_post(body=msg)
                    product_tmpl_id = produced_product.product_id.product_tmpl_id
                    product_tmpl_id.do_change_standard_price(prices['final_price'])
                self.logger.info('id:' + str(produced_product.id) + ":price:" + str(production.move_created_ids[0].price_unit))
        else:
            # we are just consuming?
            # 
            # TODO:need to set the need_to_be_costed
            pass
        for moveline in production.move_lines:
            self.logger.info('move_lineid:' + str(moveline.id))

        res = super(mrp_production, self).action_produce(production_id, production_qty, production_mode, wiz)
        # don't forget to mark them costed

        return res




# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
