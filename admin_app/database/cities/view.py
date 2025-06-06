"""database/cities"""

from starlette_admin.contrib.sqla import ModelView

from .model import CitiesTable


class CitiesView(ModelView):
    fields = [
        CitiesTable.id,
        CitiesTable.name,
        CitiesTable.created_at,
        CitiesTable.update_at,

        CitiesTable.district,
        CitiesTable.organization,
        CitiesTable.creator,
        CitiesTable.updator,
    ]

    exclude_fields_from_create = [CitiesTable.created_at, CitiesTable.update_at]
    exclude_fields_from_edit = [CitiesTable.created_at, CitiesTable.update_at]
    icon = "fa fa-building"