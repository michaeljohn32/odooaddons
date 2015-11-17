# -*- coding: utf-8 -*-
from openerp import http

# class TemplateMod(http.Controller):
#     @http.route('/template_mod/template_mod/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/template_mod/template_mod/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('template_mod.listing', {
#             'root': '/template_mod/template_mod',
#             'objects': http.request.env['template_mod.template_mod'].search([]),
#         })

#     @http.route('/template_mod/template_mod/objects/<model("template_mod.template_mod"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('template_mod.object', {
#             'object': obj
#         })