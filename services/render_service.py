def render_scoreboard(scores):
    html = '<div id="scoreboard" class="scoreboard">'

    for user, score in sorted(scores.items(), key=lambda item: item[1], reverse=True):
        html += f"""
        <div class="row">
            <img src="/static/img/{user}.jpg" class="avatar"></img>
            <span class="name">{user}</span>
            <span class="score">{scores[user]}</span>
        </div>
        """
    html += "</div>"
    return html
