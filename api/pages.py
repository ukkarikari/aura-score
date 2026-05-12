from fastapi import Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from core.templates import get_templates
from db.database import SessionLocal
from services.auth import get_current_user
from services.render_service import render_scoreboard
from services.score_service import compute_scores
from services.user_service import get_all_usernames, get_all_users, get_username_by_id

router_root = APIRouter()
router_vote_page = APIRouter()
router_login_page = APIRouter()


@router_login_page.get("/login", response_class=HTMLResponse)
def login_page(request: Request):

    templates = get_templates()

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={
            "request": request,
        },
    )


@router_vote_page.get("/vote-page", response_class=HTMLResponse)
def vote_page(request: Request, session_id: str | None = Cookie(default=None)):

    db = SessionLocal()

    templates = get_templates()
    current_user = get_current_user(db, session_id)

    # - [ ] **TODO:** change this to say "wrong login or something"
    if not current_user:
        return templates.TemplateResponse(
            request=request,
            name="login.html",
            context={"request": request},
        )

    current_username = get_username_by_id(db, current_user.id)  # pyright: ignore[reportArgumentType]
    print(current_username)

    users = get_all_users(db)

    usernames = get_all_usernames(db)
    print(usernames)

    scores = compute_scores(db)
    scoreboard_html = render_scoreboard(scores)

    # removes curr user from votign options
    options = [u for u in users if u.id != current_user.id]  # pyright: ignore[reportGeneralTypeIssues]
    print(options)

    return templates.TemplateResponse(
        request=request,
        name="vote_page.html",
        context={
            "request": request,
            "current_user": current_user,
            "options": options,
            "scoreboard": scoreboard_html,
        },
    )


@router_root.get("/", response_class=HTMLResponse)
def home(request: Request):

    templates = get_templates()

    db = SessionLocal()

    scores = compute_scores(db)
    scoreboard_html = render_scoreboard(scores)

    db.close()

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "scoreboard": scoreboard_html},
    )
