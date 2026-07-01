import math
from odoo.http import request


class PortalPaginationMixin:

    def _get_paginated_records(self, model, domain=None, page=1, limit=12, order='create_date desc'):
        domain = domain or []
        page = int(page or 1)
        limit = int(limit or 12)

        Model = request.env[model].sudo()

        total = Model.search_count(domain)

        records = Model.search(
            domain,
            order=order,
            limit=limit,
            offset=(page - 1) * limit,
        )

        total_pages = math.ceil(total / limit) if total else 1

        return {
            'records': records,
            'total': total,
            'page': page,
            'limit': limit,
            'total_pages': total_pages,
            'start': ((page - 1) * limit) + 1 if total else 0,
            'end': min(page * limit, total),
        }

    def _render_paginated_template(self, template, values):
        return request.env['ir.ui.view']._render_template(template, values)