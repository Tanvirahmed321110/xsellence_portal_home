# -*- coding: utf-8 -*-
{
    'name': "xsellence portal",

    'summary': """
        xsellence own software """,

    'description': """
        For Project Management and Support
    """,

    'author': "Tanvir Ahmed",
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
        'security/security_group.xml',
        'security/ir.model.access.csv',
        'templates/layout.xml',
        'templates/dashboard.xml',
        'templates/projects.xml',
        'templates/project_details.xml',
        'templates/tasks.xml',
        'templates/timesheets.xml',
        'templates/helpdesk.xml',
        'templates/add_task.xml',
        'templates/add_timesheet.xml',
        'templates/profile.xml',
        'templates/edit_profile.xml',
        'templates/create_project.xml',
        'templates/edit_project.xml',
        'templates/ticket_details.xml',
        'templates/task_details.xml',
        'templates/edit_task.xml',
        'templates/breadcrumb.xml',
        'templates/alert.xml',


        # views
        'views/project_inherit_view.xml',
        'views/project_task_inherit_view.xml',
        'views/hr_employee_inherit_view.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # 'xsellence_portal/static/src/css/custom_class.css',
        ],

        'web.assets_backend': [
            'xsellence_portal/static/src/css/custom_backend.css',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}