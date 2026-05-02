from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/add_timesheet',type='http',auth='public',website=True)
    def add_timesheet_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.add_timesheet_page',{})