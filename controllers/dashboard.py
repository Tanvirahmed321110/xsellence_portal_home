from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/dashboard',type='http',auth='public',website=True)
    def dashboard_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.dashboard_page',{
            'active_menu': 'dashboard',
        })