"""database/client_location"""

from starlette_admin.contrib.sqla import ModelView

from .model import ClientLocationTable


class ClientLocationView(ModelView):
    fields = [
        ClientLocationTable.id,
        ClientLocationTable.client,
        ClientLocationTable.branch,
        ClientLocationTable.organization,
        ClientLocationTable.created_at,
        ClientLocationTable.update_at
    ]

    exclude_fields_from_create = [ClientLocationTable.created_at, ClientLocationTable.update_at]
    exclude_fields_from_edit = [ClientLocationTable.created_at, ClientLocationTable.update_at]
    icon = "fa fa-map-marker"