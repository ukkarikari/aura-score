from fastapi import APIRouter, Cookie, Form
from fastapi.responses import HTMLResponse, Response

from core.users import users
from db.database import Base, SessionLocal, engine
from db.models.vote import Vote
from services.auth import get_current_user
from services.render_service import render_scoreboard
from services.score_service import compute_scores

router = APIRouter()


@router.post("/vote", response_class=HTMLResponse)
def vote(
    target: str = Form(...),
    value: str = Form(...),
    session_id: str | None = Cookie(default=None),
):
    username = get_current_user(session_id)

    # --- error handling
    if not username:
        return HTMLResponse("<p>not logged</p>")

    if target == username:
        return HTMLResponse("<p>cant vote for yourself</p>")

    if target not in users:
        return HTMLResponse("<p>invalid target</p>")

    # --- add vote to db
    db = SessionLocal()
    try:
        new_vote_row = Vote(voter_id=username, target_id=target, value=int(value))
        db.add(new_vote_row)
        db.commit()

        vote_rows = db.query(Vote).all()
        scores = compute_scores(vote_rows, users)
    finally:
        db.close()

    return render_scoreboard(scores)
