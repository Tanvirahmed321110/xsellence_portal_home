from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/helpdesk',type='http',auth='public',website=True)
    def helpdesk_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.helpdesk_page',{})