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

from odoo import models, fields,api
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta



class RealEstateProperty(models.Model):
    _name = 'real.estate.custom.property'
    _description = 'Real Estate Property'

    name = fields.Char(string='Name', required=True)
    property_type_id = fields.Many2one(comodel_name='real.estate.custom.property.type',string='Property Type')
    buyer_id = fields.Many2one(
        "res.partner",
        # readonly=True,
        copy=False,
        string="Buyer"
    )
    seller_id = fields.Many2one(
        "res.users",
        string="Seller",
        default=lambda self: self.env.user
    )
    tag_ids = fields.Many2many(
        "real.estate.custom.tag",
        string="Tags"
    )
    
    offer_ids = fields.One2many("real.estate.custom.property.offer", "property_id", string="Offer")

    description = fields.Text(string='Description',compute="_compute_description")
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

    total_area = fields.Integer(string="Total area",compute="_compute_total_area")
    best_price = fields.Integer(string="Best price",compute="_compute_best_price")
    
    @api.depends("buyer_id")
    def _compute_description(self):
        for record in self:
            record.description = "Test for partner %s" % record.buyer_id.name
    
    
    @api.depends('garden_area','living_area')
    def _compute_total_area(self):
        for obj in self:
            obj.total_area = self.garden_area + self.living_area
            
            
            
    @api.depends('offer_ids')
    def _compute_best_price(self):
        for obj in self:
            if obj.offer_ids:
                obj.best_price = max(obj.offer_ids.mapped('offer_price'))
            else:
                obj.best_price = 0 

class RealEstatePropertyType(models.Model):
    _name = 'real.estate.custom.property.type'
    # _inherit = 'mail.thread'
    _description = 'Real Estate Property Type'
    name = fields.Char(string='Name', required=True)

    
class EstatePropertyTag(models.Model):
    _name = "real.estate.custom.tag"
    _inherit = 'mail.thread'
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(
        required=True,
        tracking=True
    )
    
class EstatePropertyOffer(models.Model):
    _name = 'real.estate.custom.property.offer'
    # _inherit = 'mail.thread'
    _description = 'Real Estate Property Offer'
    
    name = fields.Char(
        required=True,
        tracking=True
    )    
    
    offer_price = fields.Integer()
    offer_status = fields.Selection([("accepted","Accepted"),("refused","Refused")], string='Offer Status')
    
    partner_id = fields.Many2one(
        'res.partner',
        required=True,
        string="Partner"
    )

    
    property_id = fields.Many2one(
        'real.estate.custom.property',
        string='Property',
        required=True, 
        )
    
    
    validity = fields.Integer(
        default = 7,
        string='Validity in days(default is 7)',
    )
    date_deadline = fields.Date(string='Date deadline',
                                compute='_compute_validity_date',
                                inverse='_inverse_validity_date'
                                )
    
    @api.depends("date_deadline","validity")
    def _compute_validity_date(self):
        for obj in self:
            if obj.create_date:
                obj.date_deadline = obj.create_date.date() + timedelta(days=obj.validity)
            else:
                obj.date_deadline = datetime.now().date() + timedelta(days=obj.validity)
                
    def _inverse_validity_date(self):
        for obj in self:
            if obj.create_date:
                obj.validity = (obj.date_deadline - obj.create_date.date()).days
