# -*- coding: utf-8 -*-
# from odoo import http


# class TestScaffoldModule(http.Controller):
#     @http.route('/test_scaffold_module/test_scaffold_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/test_scaffold_module/test_scaffold_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('test_scaffold_module.listing', {
#             'root': '/test_scaffold_module/test_scaffold_module',
#             'objects': http.request.env['test_scaffold_module.test_scaffold_module'].search([]),
#         })

#     @http.route('/test_scaffold_module/test_scaffold_module/objects/<model("test_scaffold_module.test_scaffold_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('test_scaffold_module.object', {
#             'object': obj
#         })

