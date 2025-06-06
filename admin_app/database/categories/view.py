"""database/branches"""

from starlette_admin.contrib.sqla import ModelView

from .model import CategoriesTable


class CategoriesView(ModelView):
    fields = [
        CategoriesTable.id,
        CategoriesTable.name,
        CategoriesTable.details,
        CategoriesTable.created_at,
        CategoriesTable.update_at,
        CategoriesTable.organization,
        CategoriesTable.creator,
        CategoriesTable.updator,
    ]

    exclude_fields_from_create = [CategoriesTable.created_at, CategoriesTable.update_at]
    exclude_fields_from_edit = [CategoriesTable.created_at, CategoriesTable.update_at]
    icon = "fa fa-window-restore"