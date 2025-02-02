from starlette.applications import Starlette
from starlette_admin.contrib.sqla import Admin

import database
from database.db_core import Base, engine


Base.metadata.create_all(engine)

app = Starlette()

admin = Admin(engine, title="Shelf", base_url="/")

admin.add_view(database.CustomAuthTokenTable(database.AuthTokenTable))
admin.add_view(database.CustomCustomersTable(database.CustomersTable))

admin.mount_to(app)
