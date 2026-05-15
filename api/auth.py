import uuid

from fastapi import Form
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from db.database import SessionLocal
from services.auth import sessions
from services.security import verify_password
from services.user_service import get_user_by_username

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login")
def login(
    request: Request,
    db: Session = Depends(get_db),  # pyright: ignore[reportArgumentType]
    username: str = Form(...),
    password: str = Form(...),
    response: Response = None,  # pyright: ignore[reportArgumentType]
):

    user = get_user_by_username(db, username)

    # if not user or user.password_hash != password:  # pyright: ignore[reportGeneralTypeIssues]
    #    print("------ bad login!! ----- ")
    #    response = HTMLResponse("<p>bad login</p>")
    #    response.headers["HX-Redirect"] = "/login"
    #    return response

    if not user:
        print("------ bad login!! ----- ")
        response = HTMLResponse("<p>bad login</p>")
        response.headers["HX-Redirect"] = "/login"
        return response

    if not verify_password(password, user.password_hash):  # pyright: ignore[reportArgumentType]
        print("------ bad login!! ----- ")
        response = HTMLResponse("<p>bad login</p>")
        response.headers["HX-Redirect"] = "/login"
        return response

    # request.session["user_id"] = user.id

    session_id = str(uuid.uuid4())
    sessions[session_id] = user.id

    print(type(sessions))

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/vote-page"
    response.set_cookie(key="session_id", value=session_id)

    return response
