"""database/districts"""

from starlette_admin.contrib.sqla import ModelView
from starlette_admin import FileField

from .model import DistrictsTable


class DistrictsView(ModelView):
    fields = [
        DistrictsTable.id,
        DistrictsTable.name,
        DistrictsTable.created_at,
        DistrictsTable.update_at,

        DistrictsTable.country,
        DistrictsTable.organization,
        DistrictsTable.creator,
        DistrictsTable.updator,
    ]

    exclude_fields_from_create = [DistrictsTable.created_at, DistrictsTable.update_at]
    exclude_fields_from_edit = [DistrictsTable.created_at, DistrictsTable.update_at]
    icon = "fa fa-object-group"