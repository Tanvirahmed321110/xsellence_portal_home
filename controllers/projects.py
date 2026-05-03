from odoo import http
from odoo.http import request

# For Projects Page
class XsellencePortal(http.Controller):
    @http.route('/projects',type='http',auth='public',website=True)
    def projects_f (self,**kw):
        print('load dashboard')
        return  request.render('xsellence_portal.projects_page',{
            'active_menu' : 'projects',
            'breadcrumb' : [
                {'name' : 'Dashboard', 'url': '/dashboard'},
                {'name' : 'Projects', 'url': False},
            ]
        })

    #==================  For Create Project Page  ====================
    @http.route('/create_project', type='http', auth='public', website=True)
    def create_project_f(self, **kw):
        source = kw.get('source')
        print(source)

        if source == 'projects':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Create Project', 'url':False},
            ]
        else:
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Create Project', 'url': False},
            ]

        return request.render('xsellence_portal.create_project_page', {
            'active_menu': 'projects',
            'breadcrumb': breadcrumb_data,
        })


    #=================  For Project Details Page  ===================
    # @http.route('/projects/details/<int:project_id>', type='http', auth='public', website=True)
    @http.route('/projects/project_details', type='http', auth='public', website=True)
    # def project_details_f(self, project_id, **kw):
    def project_details_f(self, **kw):
        # project = request.env['project.project'].sudo().browse(project_id)

        return request.render('xsellence_portal.project_details_page', {
            'active_menu': 'projects',
            # 'project': project,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Project Details', 'url': False}
            ]
        })