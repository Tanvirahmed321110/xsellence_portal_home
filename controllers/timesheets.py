from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/timesheets',type='http',auth='public',website=True)
    def timesheet_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.timesheet_page',{})