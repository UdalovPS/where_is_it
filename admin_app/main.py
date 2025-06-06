from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin

import database
from database.db_core import Base, engine


# Base.metadata.create_all(engine)

app = Starlette()

admin = Admin(engine, title="Shelf", base_url="/")

admin.add_view(database.UsersView(database.UsersTable, icon=database.UsersView.icon))
admin.add_view(database.AuthTokeView(database.AuthTokenTable, icon=database.AuthTokeView.icon))
admin.add_view(database.OrganizationView(database.OrganizationsTable, icon=database.OrganizationView.icon))
admin.add_view(database.CountriesView(database.CountriesTable, icon=database.CountriesView.icon))
admin.add_view(database.DistrictsView(database.DistrictsTable, icon=database.DistrictsView.icon))
admin.add_view(database.CitiesView(database.CitiesTable, icon=database.CitiesView.icon))
admin.add_view(database.BranchesView(database.BranchesTable, icon=database.BranchesView.icon))
admin.add_view(database.BranchesSchemasView(database.BranchSchemasTable, icon=database.BranchesSchemasView.icon))
admin.add_view(database.ShelvesView(database.ShelvesTable, icon=database.ShelvesView.icon))
admin.add_view(database.SpotsView(database.SpotsTable, icon=database.SpotsView.icon))
admin.add_view(database.CategoriesView(database.CategoriesTable, icon=database.CategoriesView.icon))
admin.add_view(database.ItemsView(database.ItemsTable, icon=database.ItemsView.icon))
admin.add_view(database.FrontendServicesView(database.FrontendServicesTable, icon=database.FrontendServicesView.icon))
admin.add_view(database.ClientsView(database.ClientsTable, icon=database.ClientsView.icon))
admin.add_view(database.ClientLocationView(database.ClientLocationTable, icon=database.ClientLocationView.icon))

admin.mount_to(app)
