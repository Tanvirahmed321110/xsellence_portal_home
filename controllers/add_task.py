from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/add_task',type='http',auth='public',website=True)
    def add_task_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.add_task_page',{})