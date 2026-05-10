from db.database import SessionLocal
from db.models.vote import Vote


def render_scoreboard(scores):
    html = '<div id="scoreboard" class="scoreboard">'

    db = SessionLocal()

    for user, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        latest_vote = (
            db.query(Vote)
            .filter(Vote.target_id == user)
            .order_by(Vote.created_at.desc())
            .first()
        )

        reason = latest_vote.reason if latest_vote else "null"

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
        </div>
        """
    html += "</div>"

    db.close()

    return html
