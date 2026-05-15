import uuid

from fastapi import Form
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.routing import APIRouter
from sqlalchemy.orm.session import Session

from db.database import SessionLocal
from db.models.session import Session as UserSession

# from services.auth import sessions
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

    # session_id = str(uuid.uuid4())
    # sessions[session_id] = user.id

    session_id = str(uuid.uuid4())

    db_session = UserSession(
        session_token=session_id,
        user_id=user.id,
    )

    db.add(db_session)
    db.commit()

    # print(type(sessions))

    response = HTMLResponse("")
    response.headers["HX-Redirect"] = "/vote-page"
    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=60 * 60 * 24 * 30,
    )

    return response
