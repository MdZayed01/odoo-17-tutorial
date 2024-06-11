# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class real_estate_model(models.Model):
#     _name = 'real_estate_model.real_estate_model'
#     _description = 'real_estate_model.real_estate_model'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

from odoo import models, fields
from datetime import datetime
from dateutil.relativedelta import relativedelta



class RealEstateProperty(models.Model):
    _name = 'real.estate.custom.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    postcode = fields.Char(string='Postcode')
    date_availability = fields.Date(string='Date of Availability',default =fields.Date.today() + relativedelta(months=3))
    expected_price = fields.Float(string='Expected Price', required=True,default=0.0,copy=False)
    selling_price = fields.Float(string='Selling Price',readonly=True,copy=False)
    bedrooms = fields.Integer(string='Bedrooms',default = 2)
    living_area = fields.Integer(string='Living Area (sqm)')
    facades = fields.Integer(string='Number of Facades')
    garage = fields.Boolean(string='Garage')
    garden = fields.Boolean(string='Garden')
    garden_area = fields.Integer(string='Garden Area (sqm)')
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West'),
    ], string='Garden Orientation')
    
    last_seen = fields.Datetime("Last Seen", default=fields.Datetime.now)
    
    active = fields.Boolean(default = False,string='Active')
    state = fields.Selection(string='State',required=True, selection=[
        ('new', 'New'), 
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled'),
        ]
        ,
        default = 'new'                     
        )






