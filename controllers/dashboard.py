from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):

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

        # custom group print
        # print("=" * 50)
        # print(f"User: {user.name}")
        # print("-" * 30)
        # print("Custom Groups:")
        # print(f"  - Admin: {is_admin}")
        # print(f"  - Project Manager: {is_project_manager}")
        # print(f"  - General Employee: {is_general_employee}")
        # print("-" * 30)
        # print("Built-in Groups:")
        # print(f"  - Portal User: {is_portal}")
        # print(f"  - Internal User: {is_internal}")
        # print("=" * 50)

        # user type
        if is_admin:
            user_role = 'admin'
            print("Role: ADMIN (Custom Group)")
        elif is_project_manager:
            user_role = 'project_manager'
            print("Role: PROJECT MANAGER (Custom Group)")
        elif is_general_employee:
            user_role = 'general_employee'
            print("Role: GENERAL EMPLOYEE (Custom Group)")
        elif is_internal:
            user_role = 'internal'
            print("Role: INTERNAL USER (Built-in)")
        elif is_portal:
            user_role = 'portal'
            print("Role: PORTAL USER (Built-in)")
        else:
            user_role = 'public'
            print("Role: PUBLIC USER")

        return request.render('xsellence_portal.dashboard_page', {
            'active_menu': 'dashboard',
            'user_type': user_role,
            'is_admin': is_admin,
            'is_project_manager': is_project_manager,
            'is_general_employee': is_general_employee,
        })