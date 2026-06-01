from odoo import http
from odoo.http import request


def _get_user_data():
    user = request.env.user
    employee = request.env['hr.employee'].sudo().search([
        ('user_id', '=', user.id)
    ], limit=1)
    return {
        'name':           employee.name or user.name or '',
        'work_email':     employee.work_email or user.email or '—',
        'employee_image': employee.image_128,
        'designation':    employee.job_id.name or '—',
        'department':     employee.department_id.name or '—',
        'hr_id':          employee.barcode or '—',
    }