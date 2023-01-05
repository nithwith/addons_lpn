from odoo import models, api, _, SUPERUSER_ID
from odoo.exceptions import RedirectWarning, Warning
from urllib.error import HTTPError
import urllib.request
import urllib.parse
import requests
import logging
import json
import time
import base64
import mimetypes

GOOGLE_TOKEN_ENDPOINT = "https://accounts.google.com/o/oauth2/token"
TIMEOUT = 20

CLOUDPRINT_URL = 'https://www.google.com/cloudprint'

_logger = logging.getLogger(__name__)


class Googlecloudprinterconfiguration(models.Model):
    _name = 'google.cloudprinter.configuration'

    @api.model
    def get_access_token_from_google(self, scope=None, user=None):
        config_parameter = self.env['ir.config_parameter']
        if not user:
            google_cloudprint_refresh_token = config_parameter.sudo().get_param('google_cloudprint_refresh_token')
            user_is_admin = self.env.user.id == SUPERUSER_ID
            if not google_cloudprint_refresh_token:
                if user_is_admin:
                    dummy, action_id = self.env['ir.model.data'].get_object_reference('base_setup',
                                                                                      'action_general_configuration')
                    msg = _(
                        "You haven't configured 'Authorization Code' generated"
                        " from google, Please generate and configure it .")
                    raise RedirectWarning(msg, action_id, _('Go to the configuration panel'))
                else:
                    raise Warning(_(
                        "Google Drive is not yet configured. "
                        "Please contact your administrator."))
        else:
            google_cloudprint_refresh_token = user.google_cloudprint_refresh_token

        google_cloud_printer_client_id = config_parameter.sudo().get_param('google_cloudprint_client_id')
        google_cloud_printer_client_secret = config_parameter.sudo().get_param('google_cloudprint_client_secret')

        data = urllib.parse.urlencode({
            'client_id': google_cloud_printer_client_id,
            'refresh_token': google_cloudprint_refresh_token,
            'client_secret': google_cloud_printer_client_secret,
            'grant_type': "refresh_token",
            'scope': scope or 'https://www.googleapis.com/auth/cloudprint'
        }).encode("utf-8")
        headers = {"Content-type": "application/x-www-form-urlencoded"}
        try:
            req = urllib.request.Request(GOOGLE_TOKEN_ENDPOINT, data, headers)
            content = urllib.request.urlopen(req, timeout=TIMEOUT).read()
        except HTTPError:
            if user_is_admin:
                dummy, action_id = self.env['ir.model.data'].get_object_reference('base_setup',
                                                                                  'action_general_configuration')
                msg = _(
                    "Something went wrong during the token generation. "
                    "Please request again an authorization code .")
                raise RedirectWarning(msg, action_id, _('Go to the configuration panel'))
            else:
                raise Warning(_(
                    "Google Drive is not yet configured. "
                    "Please contact your administrator."))
        content = json.loads(content.decode('utf-8'))
        return content.get('access_token')

    @api.model
    def get_response(self, interface, params=None, data=None, user=None):
        access_token = self.get_access_token_from_google(user=user)
        request_url = "%s/%s" % (CLOUDPRINT_URL, interface)
        if params:
            request_url += "?%s" % (urllib.parse.urlencode(params).encode("utf-8"))
        headers = {
            "Authorization": 'Bearer ' + access_token,
        }
        data_json = data and json.dumps(data.encode('utf-8')) or None
        try:
            req = urllib.request.Request(request_url, data_json, headers)
            response = urllib.request.urlopen(req, timeout=TIMEOUT).read()
        except HTTPError:
            raise Warning(_(
                "Could not connect to google cloud print. "
                "Check your configuration"))
        return json.loads(response.decode('utf-8'))

    @api.model
    def get_printers(self, user=None):
        return self.get_response('search', user=user).get('printers')
    @api.model
    def submit_job(self, printerid, jobtype, jobsrc, options):
        """Submit a job to printerid with content of dataUrl.

        Args:
            printerid: string, the printer id to submit the job to.
            jobtype: string, must match the dictionary keys in content and
                content_type.
            jobsrc: string, points to source for job. Could be a pathname or
                id string.
        Returns:
            boolean: True = submitted, False = errors.
        """
        if jobtype in ['qweb-pdf', 'pdf', 'aeroo']:
            jobtype = 'pdf'
        if jobtype in ['pdf', 'png', 'jpeg']:
            b64file = self.Base64Encode(jobsrc)
        else:
            raise Warning(_(
                'Jobtype %s not implemented for google cloud printing') % (
                              jobtype))

        datehour = time.strftime('%b%d%H%M', time.localtime())
        title = '%s%s' % (datehour, jobsrc)
        request_url = "%s/%s" % (CLOUDPRINT_URL, 'submit')

        session = requests.Session()
        access_token = self.get_access_token_from_google()
        headers = {
            "Authorization": 'Bearer %s' % access_token,
        }
        session.post(request_url, headers=headers)
        data = dict([
            ("printerid", '__google__docs'),
            ("title", title),
            ("contentType", 'dataUrl'),
            ('capabilities', ('capabilities', '{"capabilities":[]}',
                              'dataUrl')),
        ])
        files = [
            ('content', (None, open(b64file, 'rb'))),
            ('content', (jobsrc, open(b64file, 'rb'), 'dataUrl')),
        ]
        response = session.post(
            request_url,
            data=data,
            files=files,
            headers=headers,
        )

        status = self.Validate(response)
        if not status:
            error_msg = self.GetMessage(response)
            raise Warning(_('Print job %s failed with %s' % (jobtype, error_msg)))
        return status

    # methods adapted from
    # https://developers.google.com/cloud-print/docs/pythonCode
    @api.model
    def Validate(self, response):
        if response.content.find(b'"success": true') > 0:
            return True
        else:
            return False

    @api.model
    def GetMessage(self, response):
        """Extract the API message from a Cloud Print API json response.

        Args:
            response: json response from API request.
        Returns:
            string: message content in json response.
        """
        if response.content:
            lines = response.content.decode("utf-8").split('\n')
            for line in lines:
                if '"message":' in line:
                    msg = line.split(':')
                    return msg[1]
        return None

    @api.model
    def Base64Encode(self, pathname):
        """Convert a file to a base64 encoded file.
          Args:
            pathname: path name of file to base64 encode..
          Returns:
            string, name of base64 encoded file.
          For more info on data urls, see:
            http://en.wikipedia.org/wiki/Data_URI_scheme
        """
        b64_pathname = pathname + '.b64'
        file_type = mimetypes.guess_type(pathname)[0] or 'application/pdf'

        data = self.ReadFile(pathname)

        # Convert binary data to base64 encoded data.
        # file_type = 'application/pdf'
        header = 'data:%s;base64,' % file_type
        b64data = bytes(header, 'utf-8') + base64.b64encode(data)

        if self.WriteFile(b64_pathname, b64data):
            return b64_pathname
        else:
            return None

    @api.model
    def ReadFile(self, pathname):
        """Read contents of a file and return content.
           Args:
             pathname: string, (path)name of file.
           Returns:
           string: contents of file.
        """
        try:
            f = open(pathname, 'rb')
            try:
                s = f.read()
            except IOError as error:
                _logger.info('Error reading %s\n%s', pathname, error)
            finally:
                f.close()
                return s
        except IOError as error:
            _logger.error('Error opening %s\n%s', pathname, error)
            return None

    @api.model
    def WriteFile(self, file_name, data):
        """Write contents of data to a file_name.
          Args:
            file_name: string, (path)name of file.
            data: string, contents to write to file.
          Returns:
            boolean: True = success, False = errors.
        """
        status = True

        try:
            f = open(file_name, 'wb')
            try:
                f.write(data)
            except IOError as error:
                # logger.error('Error writing %s\n%s', file_name, error)
                status = False
            finally:
                f.close()
        except IOError as error:
            _logger.error('Error opening %s\n%s', file_name, error)
            status = False
        return status
