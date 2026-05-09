from fastapi import Cookie, Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter

from core.templates import get_templates
from core.users import users
from db.database import SessionLocal
from db.models.vote import Vote
from services.auth import get_current_user
from services.render_service import render_scoreboard
from services.score_service import compute_scores

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

    current_user = get_current_user(session_id)
    templates = get_templates()

    if not current_user:
        return HTMLResponse(
            '<p style="font-size: 20px">Please <a href="/login">login</a></p>'
        )

    db = SessionLocal()
    try:
        vote_rows = db.query(Vote).all()
    finally:
        db.close()

    scores = compute_scores(vote_rows, users)
    scoreboard_html = render_scoreboard(scores)

    options = [u for u in users if u != current_user]

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
    try:
        vote_rows = db.query(Vote).all()
    finally:
        db.close()

    scores = compute_scores(vote_rows, users)
    scoreboard_html = render_scoreboard(scores)

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"request": request, "scoreboard": scoreboard_html},
    )
