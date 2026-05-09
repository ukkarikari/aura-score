def compute_scores(votes, users):
    scores = {}

    for user in users:
        scores[user] = 0

    for vote in votes:
        scores[vote.target_id] += vote.value

    return scores
