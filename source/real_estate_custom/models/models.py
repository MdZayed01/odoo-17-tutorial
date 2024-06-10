# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class real_estate_custom(models.Model):
#     _name = 'real_estate_custom.real_estate_custom'
#     _description = 'real_estate_custom.real_estate_custom'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

