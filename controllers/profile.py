from odoo import http
from odoo.http import request

class XsellencePortal(http.Controller):
    @http.route('/profile',type='http',auth='public',website=True)
    def profle_f (self,**kw):
        return  request.render('xsellence_portal.profile_page',{})



class XsellencePortal(http.Controller):
    @http.route('/edit_profile',type='http',auth='public',website=True)
    def edit_profile (self,**kw):
        return  request.render('xsellence_portal.edit_profile_page',{})