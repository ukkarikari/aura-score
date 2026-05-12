from db.models.user import User


def get_all_users(db):
    return db.query(User).all()


def get_user_by_username(db, username: str):
    return db.query(User).filter(User.username == username).first()


def get_username_by_id(db, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    return user.username if user else None


def get_all_usernames(db):
    users = get_all_users(db)

    return [user.username for user in users]


def get_user_map(db):
    users = get_all_users(db)

    return {user.id: user.username for user in users}
