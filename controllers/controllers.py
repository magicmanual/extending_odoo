# -*- coding: utf-8 -*-
# from odoo import http


# class ExtendingOdoo(http.Controller):
#     @http.route('/extending_odoo/extending_odoo/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/extending_odoo/extending_odoo/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('extending_odoo.listing', {
#             'root': '/extending_odoo/extending_odoo',
#             'objects': http.request.env['extending_odoo.extending_odoo'].search([]),
#         })

#     @http.route('/extending_odoo/extending_odoo/objects/<model("extending_odoo.extending_odoo"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('extending_odoo.object', {
#             'object': obj
#         })
