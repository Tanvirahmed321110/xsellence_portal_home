from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):

    # ========================
    # For Dashboard Route
    # ========================
    @http.route('/dashboard', type='http', auth='user', website=True)
    def dashboard_f(self, **kw):

        user = request.env.user

        # users
        is_admin = user.has_group('xsellence_portal.group_admin')
        is_project_manager = user.has_group('xsellence_portal.group_project_manager')
        is_general_employee = user.has_group('xsellence_portal.group_general_employee')

        # group
        is_portal = user.has_group('base.group_portal')
        is_internal = user.has_group('base.group_user')


        # user type
        if is_admin:
            user_role = 'admin'
        elif is_project_manager:
            user_role = 'project_manager'
        elif is_general_employee:
            user_role = 'general_employee'
        elif is_internal:
            user_role = 'internal'
        elif is_portal:
            user_role = 'portal'
        else:
            user_role = 'public'

        active_employees = request.env['hr.employee'].sudo().search([
            ('active', '=', True),
        ],order='name asc')



        return request.render('xsellence_portal.dashboard_page', {
            'active_menu': 'dashboard',
            'user_type': user_role,
            'is_admin': is_admin,
            'is_project_manager': is_project_manager,
            'is_general_employee': is_general_employee,
            'active_employees':active_employees
        })