# -*- coding: utf-8 -*-
from openerp import http

# class MrpBomCalculation(http.Controller):
#     @http.route('/mrp_bom_calculation/mrp_bom_calculation/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_bom_calculation/mrp_bom_calculation/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_bom_calculation.listing', {
#             'root': '/mrp_bom_calculation/mrp_bom_calculation',
#             'objects': http.request.env['mrp_bom_calculation.mrp_bom_calculation'].search([]),
#         })

#     @http.route('/mrp_bom_calculation/mrp_bom_calculation/objects/<model("mrp_bom_calculation.mrp_bom_calculation"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_bom_calculation.object', {
#             'object': obj
#         })