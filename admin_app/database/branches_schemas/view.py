"""database/branches_schemas"""

from starlette_admin.contrib.sqla import ModelView

from .model import BranchSchemasTable


class BranchesSchemasView(ModelView):
    exclude_fields_from_create = [BranchSchemasTable.created_at, BranchSchemasTable.update_at]
    exclude_fields_from_edit = [BranchSchemasTable.created_at, BranchSchemasTable.update_at]
    icon = "fa fa-map"