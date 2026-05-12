from db.models.vote import Vote
from services.user_service import get_all_users


def compute_scores(db):
    scores = {}

    user_rows = get_all_users(db)
    vote_rows = db.query(Vote).all()

    user_lookup = {}

    for user in user_rows:
        scores[user.username] = 0
        user_lookup[user.id] = user.username

    for vote in vote_rows:
        username = user_lookup[vote.target_id]
        scores[username] += vote.value

    return scores
