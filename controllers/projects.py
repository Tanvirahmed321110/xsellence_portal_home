from odoo import http
from odoo.http import request
from datetime import date
from odoo.tools import html2plaintext


# ========== For Projects Page  ============
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

        projects = request.env['project.project'].sudo().search(
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
        customers = request.env['res.partner'].sudo().search([])
        project_managers = request.env['res.users'].sudo().search([('share', '=', False)])
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
            'priority': priority,
            'today': date.today().strftime('%Y-%m-%d'),
        })

    # ================== Submit Project ==================
    @http.route('/submit_project', type='http', auth='user', methods=['POST'], website=True, csrf=True)
    def submit_project(self, **post):

        assigned_user_ids = request.httprequest.form.getlist('assigned_user_ids')
        tags = request.httprequest.form.getlist('tag_ids')

        create_data = {
            'name': post.get('name'),
            'github_link': post.get('github_link'),
            'dev_link': post.get('dev_link'),
            'live_link': post.get('live_link'),
            'partner_id': post.get('partner_id') if post.get('partner_id') else False,
            'user_id': int(post.get('user_id') if post.get('user_id') else False),
            'custom_status': post.get('custom_status'),
            'date_start': post.get('date_start') or date.today(),
            'date': post.get('date') or date.today(),
            'custom_priority': post.get('custom_priority'),
            'description': post.get('description'),
            'assigned_user_ids': [(6, 0, [int(x) for x in assigned_user_ids])] if assigned_user_ids else False,
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
                'error_btn_url': '/projects/create_project',
            })

        # ✅ Success Page
        return request.render('xsellence_portal.success_page', {
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
    @http.route('/project/update_status', type='http', auth='user', csrf=True)
    def update_project_status(self, project_id=None, status=None, **kw):
        if project_id and status:
            project = request.env['project.project'].sudo().browse(int(project_id))
            project.write({'custom_status': status})

        return request.redirect(f"/projects/details/{project_id}")



    # ========================
    # GET - Edit Page Show
    # ========================
    @http.route('/project/edit/<int:project_id>', type='http', auth='user', website=True, methods=['GET'])
    def edit_project_page(self, project_id, **kwargs):

        # project fetch
        project = request.env['project.project'].sudo().browse(project_id)

        if not project.exists():
            return request.redirect('/projects')

        customers = request.env['res.partner'].sudo().search([])
        project_managers = request.env['res.users'].sudo().search([])
        users = request.env['res.users'].sudo().search([])
        tags = request.env['project.tags'].sudo().search([])

        status_field = request.env['project.project']._fields.get('custom_status')
        priority_field = request.env['project.project']._fields.get('custom_priority')
        status_selection = status_field.selection if status_field else []
        priority_selection = priority_field.selection if priority_field else []

        # project object
        return request.render('xsellence_portal.edit_project_page', {
            'project': project,
            'project_desc':html2plaintext(project.description or ''),
            'customers': customers,
            'project_managers': project_managers,
            'users': users,
            'tags': tags,
            'status_selection': status_selection,
            'priority': priority_selection,
        })

    # ========================
    # POST - Edit Page Submit
    # ========================
    @http.route('/project/edit/<int:project_id>', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def edit_project_submit(self, project_id, **kw):
        project = request.env['project.project'].sudo().browse(project_id)

        if not project.exists():
            return request.redirect('/projects')

        tag_ids = request.httprequest.form.getlist('tag_ids')
        tag_ids = [int(item) for item in tag_ids if item]

        assigned_user_ids = request.httprequest.form.getlist('assigned_user_ids')
        assigned_user_ids = [int(user) for user in assigned_user_ids if user]

        vals = {
            'name':  kw.get('name', project.name),
            'partner_id': int(kw['partner_id']) if kw.get('partner_id') else False,
            'user_id': int(kw['user_id']) if kw.get('user_id') else False,
            'date_start': kw.get('date_start') or False,
            'date': kw.get('date') or False,
            'description': kw.get('description', ''),
            'custom_status': kw.get('custom_status', ''),
            'custom_priority': kw.get('custom_priority', ''),
            'tag_ids': [(6, 0, tag_ids)],
            'assigned_user_ids': [(6, 0, assigned_user_ids)],
        }

        project.write(vals)
        return request.redirect(f"/projects/details/{project_id}")




    # ========================
    # POST - Project Delete
    # ========================
    @http.route('/project/delete', type="http", auth="user", methods=['POST'], website=True, csrf=True)
    def delete_project(self, project_id=None, **kw):

        last_id = request.session.get('last_project_id')

        # 1. Validate project_id first
        if not project_id or not str(project_id).isdigit():
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Invalid Request',
                'error_desc': 'Project ID missing or invalid.',
                'error_btn_label': 'Retry',
                'error_btn_url': f'/projects/details/{last_id}' if last_id else '/projects',
            })

        project = request.env['project.project'].sudo().browse(int(project_id))

        # 3. Get project tasks
        tasks = request.env['project.task'].sudo().with_context(active_test=False).search([
            ('project_id', '=', project.id)
        ])

        # 4. Check timesheet entries under this project/task
        timesheet_domain = [('project_id', '=', project.id)]

        if tasks:
            timesheet_domain = [
                '|',
                ('project_id', '=', project.id),
                ('task_id', 'in', tasks.ids),
            ]

        timesheet = request.env['account.analytic.line'].sudo().search(
            timesheet_domain,
            limit=1
        )

        # 5. If task + timesheet exists, do not delete
        if tasks and timesheet:
            return request.render('xsellence_portal.error_page', {
                'error_title': 'Project Cannot Be Deleted',
                'error_desc': 'This project has tasks with timesheet entries. Please remove the timesheet entries first, or archive the project instead of deleting it.',
                'error_btn_label': 'Back to Project',
                'error_btn_url': f'/projects/details/{project.id}',
            })

        # 6. Safe delete if no task timesheet exists
        project.unlink()

        return request.render('xsellence_portal.success_page', {
            'success_title': 'Project Deleted Successfully',
            'success_desc': 'The project has been permanently deleted and is no longer available.',
            'success_btn_label': 'Show All Projects',
            'success_btn_url': '/projects',
        })