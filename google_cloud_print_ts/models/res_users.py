from odoo import fields, models, api

class res_users(models.Model):
    _inherit = "res.users"

    google_cloudprint_refresh_token = fields.Char('Refresh Token from Google', readonly=True)
    google_cloud_printer_uri = fields.Char(compute='_compute_cloud_printer_uri', string='URI',
                                           help="Generate the authorization code from Google")
    google_cloudprint_authorization_code = fields.Char(string='Authorization Code')
    gcprinter_ids = fields.One2many('printing.printer', 'gc_user_id', 'Google Cloud Printers')

    def get_google_cloud_printer_scope(self):
        return (
            'https://www.googleapis.com/auth/cloudprint '
            'https://www.googleapis.com/auth/drive.readonly')

    @api.depends('google_cloudprint_authorization_code')
    def _compute_cloud_printer_uri(self):
        google_service = self.env['google.service']
        for rec in self:
            google_cloud_printer_uri = google_service._get_google_token_uri('cloudprint',
                                                                            scope=rec.get_google_cloud_printer_scope())
            rec.google_cloud_printer_uri = google_cloud_printer_uri

    @api.constrains('google_cloudprint_authorization_code')
    def set_google_cloudprint_authorization_code(self):
        google_service = self.env['google.service']
        for record in self:
            authorization_code = record.google_cloudprint_authorization_code
            if authorization_code:
                refresh_token = google_service.generate_refresh_token('cloudprint', authorization_code)
                record.google_cloudprint_refresh_token = refresh_token
            else:
                record.google_cloudprint_refresh_token = False

    @api.multi
    def update_user_google_cloud_printers(self):
        for user in self:
            if user.google_cloudprint_refresh_token:
                self.env['printing.printer'].update_google_cloud_printers(user=user)
        return {'type': 'ir.actions.act_window.none'}

    @api.multi
    def update_user_google_cloud_printers_status(self):
        for user in self:
            if user.google_cloudprint_refresh_token:
                self.env['printing.printer'].update_google_cloud_printers_status(user=user)
        return {'type': 'ir.actions.act_window.none'}
