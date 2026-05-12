from odoo import http
from odoo.http import request

from win32comext.shell.demos.servers.folder_view import tasks


#========== For Projects Page  ============
class XsellencePortal(http.Controller):
    @http.route('/projects', type='http', auth='user', website=True)
    def projects_f(self, **kw):

        domain = [('active', '=', True), ('name', '!=', 'Internal')]

        status = kw.get('status')
        print("STATUS FROM URL:", status, type(status))
        if status:
            domain.append(('custom_status', '=', status))

        # ===== Search Value =====
        search = kw.get('search')

        # ===== Search Filter =====
        if search:
            if search.isdigit():
                domain += [
                    '|',
                    ('name', 'ilike', search),
                    ('id', '=', int(search))
                ]
            else:
                domain.append(('name', 'ilike', search))

        projects = request.env['project.project'].search(domain, order='create_date desc')
        statuses = request.env['project.project']._fields['custom_status'].selection

        return request.render('xsellence_portal.projects_page', {
            'active_menu': 'projects',
            'projects': projects,
            'statuses': statuses,
            'status': status or '',
            'search': search or '',
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': False},
            ]
        })





    # ==================  For Create Project Page  ====================
    @http.route('/create_project', type='http', auth='public', website=True)
    def create_project_f(self, **kw):
        source = kw.get('source')

        tags = request.env['project.tags'].search([])
        customers = request.env['res.partner'].search([])
        project_managers = request.env['res.users'].search([('share', '=', False)])
        users = request.env['res.users'].sudo().search([
            ('share', 'in', [True, False]),
            ('id', '!=', request.env.ref('base.user_admin').id)
        ])
        status_selection = request.env['project.project']._fields['custom_status'].selection
        print(users)

        if source == 'projects':
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Create Project', 'url': False},
            ]
        else:
            breadcrumb_data = [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Create Project', 'url': False},
            ]

        return request.render('xsellence_portal.create_project_page', {
            'active_menu': 'projects',
            'breadcrumb': breadcrumb_data,
            'project_managers': project_managers,
            'status_selection': status_selection,
            'users': users,
            'tags': tags,
            'customers': customers,
        })



    # ================== Submit Project ==================
    @http.route('/submit_project', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def submit_project(self, **post):

        user_ids = request.httprequest.form.getlist('assigned_user_ids')
        tags = request.httprequest.form.getlist('tag_ids')
        print(f"user_ids   ---- {user_ids}")
        print(f"user_ids   ---- {tags}")
        print("POST DATA:", post)

        create_data = {
            'name': post.get('name'),
            'partner_id': post.get('partner_id') if post.get('partner_id') else False,
            'user_id': int(post.get('user_id') if post.get('user_id') else False),
            'custom_status': post.get('custom_status'),
            'date_start': post.get('date_start'),
            'date': post.get('date'),
            'description': post.get('description'),
            'assigned_user_ids': [(6, 0, [int(x) for x in user_ids])] if user_ids else False,
            'tag_ids': [(4, int(x), 0) for x in tags] if tags else [],
        }
        print(f"create_data ------------ {create_data}")

        project = request.env['project.project'].create(create_data)

        # ✅ Success Page
        return request.render('xsellence_portal.success_page')




    # =================  For Project Details Page  ===================
    @http.route('/projects/details/<int:project_id>', type='http', auth='user', website=True)
    def project_details_f(self, project_id, **kw):
        project = request.env['project.project'].sudo().browse(project_id)

        return request.render('xsellence_portal.project_details_page', {
            'active_menu': 'projects',
            'project': project,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Project Details', 'url': False}
            ]
        })
