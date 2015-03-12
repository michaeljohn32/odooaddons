# -*- coding: utf-8 -*-
from openerp import http

# class MrpCancelMoLine(http.Controller):
#     @http.route('/mrp_cancel_mo_line/mrp_cancel_mo_line/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_cancel_mo_line/mrp_cancel_mo_line/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_cancel_mo_line.listing', {
#             'root': '/mrp_cancel_mo_line/mrp_cancel_mo_line',
#             'objects': http.request.env['mrp_cancel_mo_line.mrp_cancel_mo_line'].search([]),
#         })

#     @http.route('/mrp_cancel_mo_line/mrp_cancel_mo_line/objects/<model("mrp_cancel_mo_line.mrp_cancel_mo_line"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_cancel_mo_line.object', {
#             'object': obj
#         })