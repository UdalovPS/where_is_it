from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin

import database
from database.db_core import Base, engine


# Base.metadata.create_all(engine)

app = Starlette()

admin = Admin(engine, title="Shelf", base_url="/")

admin.add_view(database.UsersView(database.UsersTable))
admin.add_view(database.AuthTokeView(database.AuthTokenTable))
admin.add_view(database.OrganizationView(database.OrganizationsTable))
admin.add_view(database.CountriesView(database.CountriesTable))
admin.add_view(database.DistrictsView(database.DistrictsTable))
admin.add_view(database.CitiesView(database.CitiesTable))
admin.add_view(database.BranchesView(database.BranchesTable))

admin.mount_to(app)
