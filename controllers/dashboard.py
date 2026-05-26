from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):

    @http.route('/dashboard', type='http', auth='user', website=True)
    def dashboard_f(self, **kw):
        user = request.env.user

        is_portal = user.has_group('base.group_portal')
        is_internal = user.has_group('base.group_user')

        if is_portal:
            user_type = 'portal'
            print("Portal User")
        elif is_internal:
            user_type = 'internal'
            print("Internal User")
        else:
            user_type = 'public'
            print("Public User")

        return request.render('xsellence_portal.dashboard_page', {
            'active_menu': 'dashboard',
            'user_type': user_type,
        })