"""database/countries"""

from starlette_admin.contrib.sqla import ModelView

from .model import CountriesTable


class CountriesView(ModelView):
    fields = [
        CountriesTable.id,
        CountriesTable.name,
        CountriesTable.organization,
        CountriesTable.created_at,
        CountriesTable.update_at,
        CountriesTable.creator,
        CountriesTable.updator,
    ]

    exclude_fields_from_create = [CountriesTable.created_at, CountriesTable.update_at]
    exclude_fields_from_edit = [CountriesTable.created_at, CountriesTable.update_at]
    icon = "fa fa-globe"