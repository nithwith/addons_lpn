from odoo import models, api, fields

class printerupdatewizard(models.TransientModel):
    _inherit = 'printing.printer.update.wizard'

    printer_type = fields.Selection([('gcp', 'Google Cloud Print')], required=True, default='gcp')

    @api.multi
    def action_ok(self):
        self.ensure_one()
        self.env['printing.printer'].update_google_cloud_printers()
        self.env['res.users'].search(
            [('google_cloudprint_refresh_token', '!=', False)]).update_user_google_cloud_printers()
        return {
            'name': 'Printers',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'printing.printer',
            'type': 'ir.actions.act_window',
            'target': 'current',
        }
