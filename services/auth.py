from db.models.user import User

sessions = {}


def get_current_user(db, session_id):

    if not session_id:
        return None

    user_id = sessions.get(session_id)

    if not session_id:
        return None

    curr = db.query(User).filter(User.id == user_id).first()

    return curr
