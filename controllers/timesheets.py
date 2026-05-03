from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/timesheets',type='http',auth='public',website=True)
    def timesheet_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.timesheet_page',{
            'active_menu': 'timesheets',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': False},
            ]
        })

    # For Add Timesheet Page
    @http.route('/add_timesheet', type='http', auth='public', website=True)
    def add_timesheet_f(self, **kw):
        return request.render('xsellence_portal.add_timesheet_page', {
            'active_menu': 'add_timesheet',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Timesheets', 'url': '/timesheets'},
                {'name': 'Add Timesheet', 'url': False},
            ]
        })

