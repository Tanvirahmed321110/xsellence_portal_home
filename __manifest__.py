# -*- coding: utf-8 -*-
{
    'name': "xsellence portal",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        For Project Management and Support
    """,

    'author': "Tanvir Ahmed, Fahim",
    'website': "http://www.xsellencebdltd.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr', 'hr_timesheet', 'portal','website'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'templates/layout.xml',
        'templates/dashboard.xml',
        'templates/projects.xml',
        'templates/tasks.xml',
        'templates/timesheets.xml',
        'templates/helpdesk.xml',
        'templates/add_task.xml',
        'templates/add_timesheet.xml',
        'templates/profile.xml',
        'templates/edit_profile.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'xsellence_portal_v1/static/src/css/custom_class.css',
        ],

        'web.assets_backend': [
            # 'xsellence_portal/static/src/css/backend.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}