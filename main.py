from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin
from starlette.middleware.sessions import SessionMiddleware

from api.auth import router as login_router
from api.pages import router_login_page, router_root, router_vote_page
from api.vote import router as vote_router
from db.database import Base, engine
from db.models.user import UserAdmin
from db.models.vote import VoteAdmin

app = FastAPI()
admin = Admin(app, engine)
app.mount("/static", StaticFiles(directory="static"), name="static")

# app.add_middleware(SessionMiddleware, secret_key="super-secret-random-string")

# -- endpoints --
app.include_router(vote_router)
app.include_router(login_router)

# -- pages --
app.include_router(router_vote_page)
app.include_router(router_root)
app.include_router(router_login_page)

# -- admin stuff --
admin.add_view(VoteAdmin)
admin.add_view(UserAdmin)
Base.metadata.create_all(bind=engine)
