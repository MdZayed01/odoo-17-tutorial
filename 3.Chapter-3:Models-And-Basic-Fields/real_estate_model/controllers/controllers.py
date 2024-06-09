# -*- coding: utf-8 -*-
# from odoo import http


# class RealEstateModel(http.Controller):
#     @http.route('/real_estate_model/real_estate_model', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/real_estate_model/real_estate_model/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('real_estate_model.listing', {
#             'root': '/real_estate_model/real_estate_model',
#             'objects': http.request.env['real_estate_model.real_estate_model'].search([]),
#         })

#     @http.route('/real_estate_model/real_estate_model/objects/<model("real_estate_model.real_estate_model"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('real_estate_model.object', {
#             'object': obj
#         })

