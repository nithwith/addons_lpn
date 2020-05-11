# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class Event(models.Model):
    _inherit = 'calendar.event'

    order_id = fields.Many2one('pos.quotation', string='Order Ref')
