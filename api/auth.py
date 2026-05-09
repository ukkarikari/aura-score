import uuid

from fastapi import Form
from fastapi.responses import HTMLResponse, Response
from fastapi.routing import APIRouter

from core.users import users
from services.auth import sessions

router = APIRouter()


@router.post("/login")
def login(
    username: str = Form(...), password: str = Form(...), response: Response = None
):
    user = users.get(username)

    if not user or user["password"] != password:
        return HTMLResponse("<p>bad login</p>")

    session_id = str(uuid.uuid4())
    sessions[session_id] = username

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/vote-page"
    response.set_cookie(key="session_id", value=session_id)

    return response


# @router.post("/login")
# def login(
#    username: str = Form(), password: str = Form(...), response: Response = None
# ):
#    user =
