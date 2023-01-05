# -*- coding: utf-8 -*-
##############################################################################
#
#    All Rights Reserved.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': "Google Cloud Printer Integration",
    "version": '12.0',
    'category': 'Generic Modules',
    'summary': 'Integrate Google cloud printer with Odoo for direct print',

    "depends": [
        'base_report_to_printer',
        'google_account',
        'server_mode',
    ],
    "data": [
        'views/res_users_view.xml',
        'views/printing_printer_view.xml',
        'wizards/res_config_settings_view.xml',
        'data/ir_config_parameter_data.xml',
        'data/printing_server_data.xml',
        'wizards/printing_printer_update_wizard.xml',
        'security/ir.model.access.csv',
        'security/google_cloud_print_security.xml',
    ],
    'images': ['static/description/gcp_odoo.png'],

    'author': 'Teqstars',
    'website': 'https://teqstars.com',
    'support': 'info@teqstars.com',
    'maintainer': 'Teqstars',

    "description": """
        - Direct print
        - Google cloud printer
        - Google cloud printer integration
        - GCP integration
        - GCP odoo
        - Odoo google cloud printer 
        - Google cloud printer odoo integration
        - GCP odoo integration
        - Odoo gcp integration
        - Google cloud printer connector
        - GCP connector
        - base report print
        - report print 
        - print report
        """,

    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'AGPL-3',
    'currency': 'EUR',
}