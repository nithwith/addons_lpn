# Copyright 2019 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'CRM Team Access Point',
    'version': '12.0.1.0.0',
    'author': 'Théo MARTY',
    'license': 'AGPL-3',
    'category': 'Sale',
    'website': 'https://github.com/nithwith',
    'depends': [
        'sales_team',
        'crm'
        ],
    'data': [
        'views/sales_views.xml',
        ],
    'installable': True,
    'auto_install': False,
}
