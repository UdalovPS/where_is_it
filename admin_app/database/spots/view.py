"""database/spots"""

from starlette_admin.contrib.sqla import ModelView

from .model import SpotsTable


class SpotsView(ModelView):
    fields = [
        SpotsTable.id,
        SpotsTable.item,
        SpotsTable.organization,
        SpotsTable.shelf,
        SpotsTable.cell_number,
        SpotsTable.floor_number,
        SpotsTable.created_at,
        SpotsTable.update_at,
        SpotsTable.creator,
        SpotsTable.updator,
    ]

    exclude_fields_from_create = [SpotsTable.created_at, SpotsTable.update_at]
    exclude_fields_from_edit = [SpotsTable.created_at, SpotsTable.update_at]
    icon = "fa fa-th"