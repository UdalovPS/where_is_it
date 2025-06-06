"""database/frontend_service"""

from starlette_admin.contrib.sqla import ModelView

from .model import FrontendServicesTable


class FrontendServicesView(ModelView):
    fields = [
        FrontendServicesTable.id,
        FrontendServicesTable.name,
        FrontendServicesTable.type,
        FrontendServicesTable.organization,
    ]
    icon = "fa fa-list-ol"