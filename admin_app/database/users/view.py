"""database/users"""

from starlette_admin.contrib.sqla import ModelView

from .model import UsersTable


class UsersView(ModelView):
    fields = [
        UsersTable.id,
        UsersTable.login,
        UsersTable.email,
        UsersTable.password,
        UsersTable.phone,
        UsersTable.role,
        UsersTable.verify,
        UsersTable.blocked,
        UsersTable.created_at
    ]
    exclude_fields_from_create = [UsersTable.created_at]
    exclude_fields_from_edit = [UsersTable.created_at]

    icon = "fa fa-users"
