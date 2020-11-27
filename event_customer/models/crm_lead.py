# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import logging
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, SUPERUSER_ID

_logger = logging.getLogger(__name__)

class Lead(models.Model):
    _inherit = "crm.lead"

    @api.multi
    def action_schedule_meeting(self):
        """ Open meeting's calendar view to schedule meeting with default value for customer"""

        action = super(Lead, self).action_schedule_meeting()
        action['context']['default_customer_id'] = self.partner_id.id
        action['context']['default_description'] = self.description
        action['context']['default_partner_ids'] = [self.user_id.partner_id.id]
        action['context']['default_partner_id'] = False
        return action

