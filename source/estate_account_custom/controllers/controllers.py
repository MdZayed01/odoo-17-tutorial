# -*- coding: utf-8 -*-
# from odoo import http


# class EstateAccountCustom(http.Controller):
#     @http.route('/estate_account_custom/estate_account_custom', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/estate_account_custom/estate_account_custom/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('estate_account_custom.listing', {
#             'root': '/estate_account_custom/estate_account_custom',
#             'objects': http.request.env['estate_account_custom.estate_account_custom'].search([]),
#         })

#     @http.route('/estate_account_custom/estate_account_custom/objects/<model("estate_account_custom.estate_account_custom"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('estate_account_custom.object', {
#             'object': obj
#         })

