from db.models.session import Session
from db.models.user import User

sessions = {}


def get_current_user(db, session_token):

    if not session_token:
        return None

    db_session = (
        db.query(Session).filter(Session.session_token == session_token).first()
    )

    if not db_session:
        return None

    return db_session.user
