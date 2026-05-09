sessions = {}


def get_current_user(session_id: str | None):
    if not session_id:
        return None
    return sessions.get(session_id)
