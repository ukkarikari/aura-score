from fastapi import APIRouter, Cookie, Form
from fastapi.responses import HTMLResponse, Response

from db.database import Base, SessionLocal, engine
from db.models.vote import Vote
from services.auth import get_current_user
from services.render_service import render_scoreboard
from services.score_service import compute_scores
from services.user_service import get_user_map

router = APIRouter()


@router.post("/vote", response_class=HTMLResponse)
def vote(
    target: int = Form(...),
    value: str = Form(...),
    reason: str = Form(...),
    session_id: str | None = Cookie(default=None),
):

    db = SessionLocal()

    current_user = get_current_user(db, session_id)
    users = get_user_map(db)
    # print(f"users: {users}")

    # --- error handling
    if not current_user:
        return HTMLResponse("<p>not logged</p>")

    if target == current_user.id:
        return HTMLResponse("<p>cant vote for yourself</p>")

    if target not in users:
        print(f"target {target}")
        return HTMLResponse("<p>invalid target</p>")

    # --- add vote to db
    try:
        new_vote_row = Vote(
            voter_id=current_user.id,
            target_id=target,
            value=int(value),
            reason=(reason),
        )
        db.add(new_vote_row)
        db.commit()

        scores = compute_scores(db)
    finally:
        db.close()

    return render_scoreboard(scores)
