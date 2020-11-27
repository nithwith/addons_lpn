# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class Event(models.Model):
    _inherit = 'calendar.event'

    #Customer
    customer_id = fields.Many2one('res.partner', 'Customer', track_visibility='onchange')
    customer_email = fields.Char('Customer Email', related='customer_id.email', readonly=True)
    customer_phone = fields.Char('Customer phone', related='customer_id.phone', readonly=True)
    #Sale
    quotation_id = fields.Many2one('pos.quotation', string='Quotation', track_visibility='onchange')
    sale_order_id = fields.Many2one('sale.order', string='Sale order', track_visibility='onchange')
