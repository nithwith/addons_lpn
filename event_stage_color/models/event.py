# -*- coding: utf-8 -*-
from odoo.exceptions import UserError
from odoo import models, fields, api, _

class EventStage(models.Model):
    _name = 'calendar.event.stage'
    _description = 'Event Stage'

    name = fields.Char(string='Stage Name', required=True, translate=True)
    color = fields.Char('Color Index', required=True)

class Event(models.Model):
    _inherit = 'calendar.event'


    def _default_stage(self):
        return self.env['calendar.event.stage'].search([], limit=1).id

    stage_id = fields.Many2one('calendar.event.stage', string='Stage', track_visibility='onchange', default=_default_stage)
    stage_color = fields.Char('Color Index', related='stage_id.color')