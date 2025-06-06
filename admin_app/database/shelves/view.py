"""database/shelves"""

from starlette_admin.contrib.sqla import ModelView

from .model import ShelvesTable


class ShelvesView(ModelView):
    fields = [
        ShelvesTable.id,
        ShelvesTable.name,
        ShelvesTable.x1,
        ShelvesTable.y1,
        ShelvesTable.x2,
        ShelvesTable.y2,
        ShelvesTable.cell_count,
        ShelvesTable.floor_count,
        ShelvesTable.created_at,
        ShelvesTable.update_at,
        ShelvesTable.organization,
        ShelvesTable.branch,
        ShelvesTable.creator,
        ShelvesTable.updator,
    ]

    exclude_fields_from_create = [ShelvesTable.created_at, ShelvesTable.update_at]
    exclude_fields_from_edit = [ShelvesTable.created_at, ShelvesTable.update_at]
    icon = "fa fa-bars"