from odoo import http
from odoo.http import request


class XsellencePortal(http.Controller):
    @http.route('/helpdesk', type='http', auth='public', website=True)
    def helpdesk_f(self, **kw):
        print('load dashboard')
        return request.render('xsellence_portal.helpdesk_page', {
            'active_menu': 'helpdesk',
        })

    # =================  Ticket Details Page  ==================
    @http.route('/helpdesk/ticket_details', type='http', auth='public', website=True)
    def ticket_details_f(self, **kw):
        print('load dashboard')
        return request.render('xsellence_portal.ticket_details_page', {
            'active_menu': 'helpdesk',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Helpdesk', 'url': '/helpdesk'},
                {'name': 'Ticket Details','url': False},
            ]
        })

    # =================  Create Ticket Page  ==================
    @http.route('/helpdesk/create_ticket', type='http', auth='user', website=True)
    def ticket_details_f(self, **kw):
        print('load dashboard')
        return request.render('xsellence_portal.create_ticket_page', {
            'active_menu': 'helpdesk',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Helpdesk', 'url': '/helpdesk'},
                {'name': 'Create Ticket ', 'url': False},
            ]
        })
