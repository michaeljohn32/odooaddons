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