from db.database import SessionLocal
from db.models.vote import Vote
from services.score_service import get_user_score_percentage
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
        # ----------------------------

        # this is even more chinese!!! change later!!!
        percentage = get_user_score_percentage(db, user)
        diff = "😎" if percentage > 25.00 else "🤢" if percentage < 5.00 else "😐"

        # ----------------------------

        html += f"""
        <div class="row">

            <div class="avatar_name">
                <img src="/static/img/{user}.jpg" class="avatar"/>
                <p style="font-size: 1.0em; color: black;">{user}</p>
            </div>

            <div class="score-section">
            <br>
                <span class="score" style="font-size: 2.0em; color: white">
                    {scores[user]}
                </span>
                <br><br>
                <span class="reason" style="font-size: 1.4em; color: black">
                    {latest_vote.reason if latest_vote else "null"}
                 </span>
                <div class="voter" style="font-size: 1.0em; color: #111111">
                    voter: {latest_vote.voter.username if latest_vote else "null"}
                 </div>
            </div>

            <div class="aura_diff" style="align: center">
                <div class="diff" style="font-size: 1.5em">
                    {diff}
                </div>
                <div>
                    {"%.1f" % percentage} %
                </div>
            </div>

            <!-- (for later) <span class="score">{"%.2f" % scores[user]} %</span> -->

        </div>
        """
    html += "</div>"

    db.close()

    return html


# --- to add: render_scoreboard_voting
def render_voting_scoreboard(scores):
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
        # ----------------------------

        # this is even more chinese!!! change later!!!
        percentage = get_user_score_percentage(db, user)
        diff = "😎" if percentage > 25.00 else "🤢" if percentage < 5.00 else "😐"

        # ----------------------------

        html += f"""
        <div class="row-voting"
            onclick="openVoteModal('{user}', {target_user.id})" style="cursor: pointer;">

            <div class="avatar_name">
                <img src="/static/img/{user}.jpg" class="avatar"/>
                <p style="font-size: 1.0em; color: black;">{user}</p>
            </div>

            <div class="score-section">
            <br>
                <span class="score" style="font-size: 2.0em; color: white">
                    {scores[user]}
                </span>
                <br><br>
                <span class="reason" style="font-size: 1.4em; color: black">
                    {latest_vote.reason if latest_vote else "null"}
                 </span>
                <div class="voter" style="font-size: 1.0em; color: #111111">
                    voter: {latest_vote.voter.username if latest_vote else "null"}
                 </div>
            </div>

            <div class="aura_diff" style="align: center">
                <div class="diff" style="font-size: 1.5em">
                    {diff}
                </div>
                <div>
                    {"%.1f" % percentage} %
                </div>
            </div>

            <!-- (for later) <span class="score">{"%.2f" % scores[user]} %</span> -->

        </div>

        """
    html += "</div>"

    db.close()

    return html
