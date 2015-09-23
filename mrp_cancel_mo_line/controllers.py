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