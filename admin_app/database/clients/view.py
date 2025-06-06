"""database/clients"""

from starlette_admin.contrib.sqla import ModelView

from .model import ClientsTable


class ClientsView(ModelView):
    fields = [
        ClientsTable.id,
        ClientsTable.name,
        ClientsTable.frontend_id,
        ClientsTable.frontend_data,
        ClientsTable.created_at,
        ClientsTable.update_at,
        ClientsTable.frontend,
    ]

    exclude_fields_from_create = [ClientsTable.created_at, ClientsTable.update_at]
    exclude_fields_from_edit = [ClientsTable.created_at, ClientsTable.update_at]
    icon = "fa fa-bug"