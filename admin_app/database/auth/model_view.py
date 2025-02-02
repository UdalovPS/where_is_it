"""database/auth"""

from starlette_admin.contrib.sqla import ModelView

from .model import AuthTokenTable


class CustomAuthTokenTable(ModelView):
    fields = [
        AuthTokenTable.id,
        AuthTokenTable.token,
        AuthTokenTable.name,
        AuthTokenTable.customer,
        AuthTokenTable.details,
        AuthTokenTable.created_at,
        AuthTokenTable.update_at
    ]
    exclude_fields_from_create = [AuthTokenTable.created_at, AuthTokenTable.update_at, AuthTokenTable.token]
    exclude_fields_from_edit = [AuthTokenTable.created_at, AuthTokenTable.update_at]
