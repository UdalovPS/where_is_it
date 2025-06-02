"""database/organizations"""

from starlette_admin.contrib.sqla import ModelView

from .model import OrganizationsTable


class OrganizationView(ModelView):
    fields = [
        OrganizationsTable.id,
        OrganizationsTable.name,
        OrganizationsTable.detail,
        OrganizationsTable.access_at,
        OrganizationsTable.created_at,
        OrganizationsTable.update_at,
        OrganizationsTable.creator,
        OrganizationsTable.updator
    ]

    exclude_fields_from_create = [OrganizationsTable.created_at, OrganizationsTable.update_at]
    exclude_fields_from_edit = [OrganizationsTable.created_at, OrganizationsTable.update_at]

