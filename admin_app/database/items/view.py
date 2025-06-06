"""database/items"""

from starlette_admin.contrib.sqla import ModelView

from .model import ItemsTable


class ItemsView(ModelView):
    fields = [
        ItemsTable.id,
        ItemsTable.sub_id,
        ItemsTable.name,
        ItemsTable.details,
        ItemsTable.created_at,
        ItemsTable.update_at,
        ItemsTable.category,
        ItemsTable.organization,
        ItemsTable.creator,
        ItemsTable.updator,
    ]

    exclude_fields_from_create = [ItemsTable.created_at, ItemsTable.update_at]
    exclude_fields_from_edit = [ItemsTable.created_at, ItemsTable.update_at]
    icon = "fa fa-inbox"