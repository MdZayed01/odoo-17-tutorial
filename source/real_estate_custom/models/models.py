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
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError
from odoo.tools.float_utils import float_compare,float_is_zero


class RealEstateProperty(models.Model):
    _name = 'real.estate.custom.property'
    _description = 'Real Estate Property'
    _order = "id desc"

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
        string="Salesman",
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
    selling_price = fields.Float(string='Selling Price',copy=False)
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
    state = fields.Selection(string='Status',readonly=True,required=True, selection=[
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
    
    
    property_type_id = fields.Many2one(
        "real.estate.custom.property.type",
        string="Property Type"
    )
    
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
                
                
    @api.onchange('garden')
    def _onchange_garden(self):
        for obj in self:
            if obj.garden:
                obj.garden_area = 10
                obj.garden_orientation = "north"
           
            else:
                obj.garden_area = 0
                obj.garden_orientation = None
                
                
    def action_set_sold(self):
        for obj in self:
            if obj.state == 'canceled':
                raise UserError('Canceled properties cannot be sold.')
            else:
                obj.state = 'sold'
        return True
                
    
    def action_set_canceled(self):
        for obj in self:
            if obj.state == 'sold':
                raise UserError("Sold properties cannot be canceled.")
            else:
                obj.state = 'canceled'
        return True
    
    _sql_constraints = [
        (
        'check_expected_price', 'CHECK(expected_price >= 0)',
        'A property expected price must be strictly positive!!'
        ),                 
        (
        'check_selling_price', 'CHECK(selling_price >= 0)',
            'A property selling price must be strictly positive!!'
        )
    ]
    
    @api.constrains('expected_price', 'selling_price')
    def _check_prices(self):
        for record in self:
            threshold_price = record.expected_price * 0.9
            if float_compare(record.selling_price, threshold_price, precision_digits=2) < 0 and not float_is_zero(record.selling_price, precision_digits=2):
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.") 

class RealEstatePropertyType(models.Model):
    _name = 'real.estate.custom.property.type'
    # _inherit = 'mail.thread'
    _description = 'Real Estate Property Type'
    _order = "name"
    name = fields.Char(string='Name', required=True)
    
    property_ids = fields.One2many('real.estate.custom.property', 'property_type_id', string='Property Ids')
    sequence = fields.Integer('Sequence', default=1, help="Used to order stages. Lower is better.")
    

    _sql_constraints = [
        (
            'property_type_unique',
            'unique(name)',
            'A property type name must be unique!!!!'
        ),
    ]    

    
class EstatePropertyTag(models.Model):
    _name = "real.estate.custom.tag"
    _inherit = 'mail.thread'
    _description = "Estate Property Tag Model"
    _order = "name"

    name = fields.Char(
        required=True,

    )
    
    color = fields.Integer("Color")
    
    _sql_constraints = [
        (
            'property_tag_unique',
            'unique(name)',
            'A property tag name must be unique!!!!'
        ),
    ]    

    
class EstatePropertyOffer(models.Model):
    _name = 'real.estate.custom.property.offer'
    # _inherit = 'mail.thread'
    _description = 'Real Estate Property Offer'
    _order = "offer_price desc"
    
    name = fields.Char(
        required=True,
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
    
    property_type_id = fields.Many2one(
        related="property_id.property_type_id",
        store=True
    )
    @api.depends("validity")
    def _compute_validity_date(self):
        for obj in self:
            if obj.create_date:
                obj.date_deadline = obj.create_date.date() + timedelta(days=obj.validity)
            else:
                obj.date_deadline = datetime.now().date() + timedelta(days=obj.validity)

    def _inverse_validity_date(self):
        # breakpoint()
        for obj in self:
            if obj.date_deadline:
                obj.validity = (obj.date_deadline - datetime.now().date()).days
            else:
                obj.validity = 7
                
    def action_offer_accept(self):
        for obj in self:      
            obj.offer_status = "accepted"
            obj.property_id.buyer_id = obj.partner_id.id
            obj.property_id.selling_price = obj.offer_price
            obj.property_id.state = "offer_accepted"
    
    
    def action_offer_refused(self):
        for obj in self:
            obj.offer_status = "refused"
            obj.property_id.buyer_id = None
            obj.property_id.selling_price = None
            obj.property_id.state = "new"
            
            
    _sql_constraints = [
        (
            'offer_price_greater_than_zero',
            'CHECK(offer_price>0)',
            'An offer price must be strictly positive!!!!'
        ),
    ]    
