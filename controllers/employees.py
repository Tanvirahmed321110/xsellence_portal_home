from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):

    @http.route('/employees', type='http', auth='user', website=True)
    def dashboard_f(self, **kw):
        return request.render('xsellence_portal.employees_page', {
            'active_menu': 'employees',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Employees', 'url': False},
            ]
        })