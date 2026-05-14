import math

from sqlalchemy.sql import func

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


# # ==== sketch for new version... future. ====
# TOTAL_SCORE = 100.0
# BASE_WEIGHT = 1
# MIN_WEIGHT = 0.1
#
#
# def compute_scores(db):
#     scores = {}
#
#     users = get_all_users(db)
#
#     # get vote sums grouped by target user
#     vote_totals = dict(
#         db.query(Vote.target_id, func.coalesce(func.sum(Vote.value), 0))
#         .group_by(Vote.target_id)
#         .all()
#     )
#
#     # compute weights
#     weights = {}
#
#     for user in users:
#         net_votes = vote_totals.get(user.id, 0)
#
#         # base rep + votes
#         weight = BASE_WEIGHT + net_votes
#
#         # normalize for negative or nil weights
#         weight = max(MIN_WEIGHT, weight)
#
#         weights[user.username] = weight
#
#     total_weight = sum(weights.values())
#
#     print("--------")
#     print(f"total_weight={total_weight}\n")
#     for user in users:
#         print(f"{user.username} weight={weights[user.username]}")
#     print("--------")
#
#     for username, weight in weights.items():
#         scores[username] = (weight / total_weight) * TOTAL_SCORE
#
#     return scores
#
