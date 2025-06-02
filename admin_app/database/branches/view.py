"""database/branches"""

from starlette_admin.contrib.sqla import ModelView

from .model import BranchesTable


class BranchesView(ModelView):
    fields = [
        BranchesTable.id,
        BranchesTable.name,
        BranchesTable.address,
        BranchesTable.city,
        BranchesTable.organization,
        BranchesTable.creator,
        BranchesTable.updator,
    ]

    exclude_fields_from_create = [BranchesTable.created_at, BranchesTable.update_at]
    exclude_fields_from_edit = [BranchesTable.created_at, BranchesTable.update_at]
