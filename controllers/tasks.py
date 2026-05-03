from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/tasks',type='http',auth='public',website=True)
    def tasks_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.tasks_page',{})