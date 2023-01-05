from odoo import fields, models, api, _
from tempfile import mkstemp
from odoo.addons.server_mode.mode import get_mode
import os
import logging

_logger = logging.getLogger(__name__)


class PrintingPrinter(models.Model):
    _inherit = "printing.printer"

    gc_user_id = fields.Many2one('res.users', 'Google Cloud User')
    printer_type = fields.Selection([('gcp', 'Google Cloud Print')], required=True, default='gcp')
    uri = fields.Char(help='Google printer id')

    @api.model
    def get_gc_printer(self, uri, user=None):
        printer = self.env['printing.printer'].search(
            [('uri', '=', uri), ('gc_user_id', '=', user and user.id or False)], limit=1)
        return printer

    @api.model
    def update_google_cloud_printers(self, user=None):
        gc_server = self.env.ref('google_cloud_print_ts.printing_server_cloudprint')
        google_printers = self.env['google.cloudprinter.configuration'].get_printers(user)
        for google_printer in google_printers:
            printer = self.get_gc_printer(google_printer.get('id'), user)
            if not printer and google_printer.get('id') != '__google__docs':
                printer.create({
                    'name': "%s%s" % (google_printer['displayName'], user and ' ' + user.name or ''),
                    'system_name': "%s%s" % (google_printer['name'], user and ' ' + user.name or ''),
                    'model': google_printer.get('type', False),
                    'location': google_printer.get('proxy', False),
                    'uri': google_printer.get('id', False),
                    'printer_type': 'gcp',
                    'status': self.get_gc_printer_status(google_printer.get('connectionStatus', False)),
                    'gc_user_id': user and user.id or False,
                    'status_message': google_printer.get('connectionStatus', False),
                    'server_id': gc_server.id,
                })
        return True

    @api.model
    def update_printers_status(self):
        self.update_google_cloud_printers_status()
        self.env['res.users'].search(
            [('google_cloudprint_refresh_token', '!=', False)]).update_user_google_cloud_printers_status()
        return True

    @api.model
    def get_gc_printer_status(self, connectionstatus):
        if connectionstatus == 'ONLINE':
            status = 'available'
        else:
            status = 'unknown'
        return status

    @api.model
    def update_google_cloud_printers_status(self, user=None):
        gcprinters = self.env['google.cloudprinter.configuration'].get_printers(user)
        for gcprinter in gcprinters:
            printer = self.get_gc_printer(gcprinter.get('id'), user)
            if printer:
                vals = {'status': self.get_gc_printer_status(gcprinter.get('connectionStatus', False))}
                printer.write(vals)

    @api.multi
    def print_document(self, report, content, **print_opts):
        if len(self) != 1:
            _logger.error(
                'Google cloud print called with %s but singleton is'
                'expeted. Check printers configuration.' % self)
            return super(PrintingPrinter, self).print_document(
                report, content, **print_opts)
        if self.printer_type != 'gcp':
            return super(PrintingPrinter, self).print_document(
                report, content, **print_opts)
        if get_mode():
            _logger.warning(_(
                "You Can not Send Mail Because Odoo is not in Production "
                "mode"))
            return True

        fd, file_name = mkstemp()
        try:
            os.write(fd, content)
        finally:
            os.close(fd)

        options = self.print_options(report, **print_opts)
        _logger.debug(
            'Going to Print via Google Cloud Printer %s' % (self.system_name))

        try:
            self.env['google.cloudprinter.configuration'].submit_job(self.uri,options.get('format', 'pdf'),file_name,options,)
            _logger.info("Printing Job: '%s'" % (file_name))
        except Exception as e:
            _logger.error(
                'Could not submit job to google cloud. This is what we get:\n'
                '%s' % e)
        return True

    @api.multi
    def enable(self):
        gc_server = self.env.ref('google_cloud_print_ts.printing_server_cloudprint')
        for printer in self:
            if printer.server_id == gc_server:
                printer.update_printers_status()
            else:
                super(PrintingPrinter, self).enable()
        return True
