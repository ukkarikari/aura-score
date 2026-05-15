from db.database import SessionLocal
from db.models.vote import Vote
from services.user_service import get_user_by_username


def render_scoreboard(scores):
    html = '<div id="scoreboard" class="scoreboard">'

    db = SessionLocal()

    for user, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        # this is very chiense we need to change it later!!!
        # maybe make it a function in score serrvice or somethiign
        # ------ THIS VVVVVVVVV -----
        target_user = get_user_by_username(db, user)
        latest_vote = (
            db.query(Vote)
            .filter(Vote.target_id == target_user.id)
            .order_by(Vote.created_at.desc())
            .first()
        )
        reason = latest_vote.reason if latest_vote else "null"
        # ----------------------------

        html += f"""
        <div class="row">
            <img src="/static/img/{user}.jpg" class="avatar"/>
            <div class="name">
            {user}
            <br>
                 <span class="reason" style="font-size: 0.6em; color: black">
                    {reason}
                 </span>
            </div>

            <span class="score">{scores[user]}</span>
            <!-- (for later) <span class="score">{"%.2f" % scores[user]} %</span> -->
        </div>
        """
    html += "</div>"

    db.close()

    return html


# --- to add: render_scoreboard_voting
