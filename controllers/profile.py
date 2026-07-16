from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):

    # ========================
    # For Profile Route
    # ========================
    @http.route('/profile', type='http', auth='user', website=True)
    def profle_f(self, **kw):
        user = request.env.user
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', user.id)], limit=1)

        print(employee.name,employee.user_id)
        print("User ID:", user.id)
        print("User Login:", user.login)
        print("Employee:", employee)
        print("Employee Name:", employee.name)

        return request.render('xsellence_portal.profile_page', {
            'user': user,
            'employee': employee,
            'active_menu': 'profile',
        })

    # ========================
    # For Profile Edit Route
    # ========================
    @http.route('/edit_profile', type='http', auth='public', website=True)
    def edit_profile(self, **kw):
        return request.render('xsellence_portal.edit_profile_page', {
            'active_menu': 'profile',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Profile', 'url': '/profile'},
                {'name': 'Edit Profile', 'url': False}
            ]
        })
