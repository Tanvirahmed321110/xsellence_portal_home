from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/projects',type='http',auth='public',website=True)
    def projects_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.projects_page')