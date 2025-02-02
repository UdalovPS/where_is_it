"""database/customer"""

from starlette_admin.contrib.sqla import ModelView

from .model import CustomersTable


class CustomCustomersTable(ModelView):
    fields = [
        CustomersTable.id,
        CustomersTable.name,
        CustomersTable.phone,
        CustomersTable.email,
        CustomersTable.login,
        CustomersTable.password,
        CustomersTable.access_at
    ]
