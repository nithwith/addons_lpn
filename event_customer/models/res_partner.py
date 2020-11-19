# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    meetings_customer_count = fields.Integer("Events", compute='_compute_meetings_customer_count',
                                 help="Number of events the partner is customer.")


    def _compute_meetings_customer_count(self):
        for partner in self:
            partner.meetings_customer_count = self.env['calendar.event'].search_count([('customer_id', '=', partner.id)])

    @api.multi
    def open_meetings(self):
        action = self.env.ref('calendar.action_calendar_event').read()[0]
        action['context'] = {
            'default_customer_id': self.id,
        }
        return action