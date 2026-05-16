from odoo import http
from odoo.http import request
from datetime import date


#========== For Projects Page  ============
class XsellencePortal(http.Controller):

    @http.route('/projects', type='http', auth='user', website=True)
    def projects_f(self, **kw):

        base_domain = [
            ('active', '=', True),
            ('name', '!=', 'Internal')
        ]

        status_domain = []

        # ===== Status Filter =====
        status = kw.get('status')
        if status:
            status_domain = [('custom_status', '=', status)]


        # ===== Final Domain Merge =====
        domain = base_domain + status_domain

        projects = request.env['project.project'].search(
            domain,
            order='create_date desc'
        )

        statuses = request.env['project.project']._fields['custom_status'].selection

        return request.render('xsellence_portal.projects_page', {
            'active_menu': 'projects',
            'projects': projects,
            'statuses': statuses,
            'status': status or '',
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
        priority = request.env['project.project']._fields['custom_priority'].selection
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
            'priority':priority,
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
            'github_link': post.get('github_link'),
            'dev_link': post.get('dev_link'),
            'live_link': post.get('live_link'),
            'partner_id': post.get('partner_id') if post.get('partner_id') else False,
            'user_id': int(post.get('user_id') if post.get('user_id') else False),
            'custom_status': post.get('custom_status'),
            'date_start': post.get('date_start') or  date.today(),
            'date': post.get('date'),
            'custom_priority': post.get('custom_priority'),
            'description': post.get('description'),
            'assigned_user_ids': [(6, 0, [int(x) for x in user_ids])] if user_ids else False,
            'tag_ids': [(4, int(x), 0) for x in tags] if tags else [],
        }
        print(f"create_data ------------ {create_data}")

        project = request.env['project.project'].create(create_data)

        # ❌  Error Page
        if not project:
            return request.render('xsellence_portal.error_page', {
                'error_title': '❌ Project Creation Failed',
                'error_desc': 'Unable to create project.',
                'error_btn_label': 'Again Try',
                'error_btn_url':  '/projects/create_project',
            })

        # ✅ Success Page
        return request.render('xsellence_portal.success_page',{
            'success_title': 'Project Successfully Created',
            'success_desc': 'Your project has been created successfully. You can now manage it and assign tasks to your team.',
            'success_btn_label': 'Show Projects',
            'success_btn_url': '/projects',
        })




    # =================  For Project Details Page  ===================
    @http.route('/projects/details/<int:project_id>', type='http', auth='user', website=True)
    def project_details_f(self, project_id, **kw):

        request.session['last_project_id'] = project_id

        project = request.env['project.project'].sudo().browse(project_id)

        status_selection = request.env['project.project'].fields_get(
            ['custom_status'])['custom_status']['selection']

        return request.render('xsellence_portal.project_details_page', {
            'active_menu': 'projects',
            'project': project,
            'status_selection': status_selection,
            'breadcrumb': [
                {'name': 'Dashboard', 'url': '/dashboard'},
                {'name': 'Projects', 'url': '/projects'},
                {'name': 'Project Details', 'url': False}
            ]
        })



    # =================  For Project Details Page State Update  ===================
    @http.route('/project/update_status', type='http', auth='user', methods=['POST'], csrf=True)
    def update_project_status(self, project_id=None, status=None, **kw):
        if project_id and status:
            project = request.env['project.project'].sudo().browse(int(project_id))
            project.write({'custom_status': status})

        return request.redirect(f"/projects/details/{project_id}")





    # =================  For Project Details Page Delete Project  ===================
    @http.route('/project/delete',type="http",auth="user",methods=['POST'])
    def delete_project(self,project_id=None,**kw):

        last_id = request.session.get('last_project_id')

        if project_id:
            project = request.env['project.project'].sudo().browse(int(project_id))
            project.unlink()

        if not project_id:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Invalid Request',
                'error_desc': 'Project ID missing.',
                'error_btn_label': 'Retry',
                'error_btn_url': f'/projects/details/{last_id}',
            })

        # ✅ Success Page
        return request.render('xsellence_portal.success_page',{
            'success_title': 'Project Deleted Successfully 🗑️',
            'success_desc': 'Your project has been created successfully. You can now manage it and assign tasks to your team.',
            'success_btn_label': 'Show All Projects',
            'success_btn_url': '/projects',
        })
