
<div align="center">

# aura score architecture documentation

</div>

---

<div align="center">

  ## api/

endpoints in here
</div>

### api/auth.py
- `/login` POST endpoint
  checks use and compares with password in the `users` dict. then assigns a session id to the username. returns a "bad login" html if password doesnt match. redirects to `/vote-page` if successful
- [ ] **TODO:** add password hashing instead of reading plaintext

### api/vote.py
- `/vote` POST endpoint
  does some validation (like if the current_user isnt the target user) and commits the new vote to the db. returns an instance of `render_scoreboard()` with the updated scores
  - [ ] *TODO:* change this to just return a change of states or smt. updates to `render_scoreboard()` should be managed by the render function
  - [x] *TODO:* update endpoint to accept vote reason
  - [ ] *TODO:* add timeout service to this endpoint! prevent spam

### api/pages.py
- `/login` GET endpoint
  - returns the login page jinja template. no context besides request.
- `/vote-page` GET endpoint
  - queries current `user.id` of user currently voting, queries `render_scoreboard(scores)` for the `scoreboard_html`, not allowing user to vote for themselves
  - [x] *TODO:* add vote reason text box
  - [ ] *TODO:* replace form with: 
    - "+" "-" buttons in each row 
    - on clicking a button, a pop up window appears with a text box (reason input) and a 'submit' button
    - some sort of feedback afterwards
  - [x] *TODO:* update to use new user model instead of `users` dict
  - [ ] *TODO:* (maybe) add timeout element modifier to page
- `/` GET endpoint
  - calculates `scores` using `scoring_service.py`
  - queries `render_scoreboard(scores)` for the `scoreboard_html`,
  - then passes both as context to the index jinja template and returns it.


<div align="center">

  ## core/

</div>

### core/templates.py
literally just:
```
def get_templates():
    return Jinja2Templates(directory="templates")
```
returns the templates defined in `templates/`

<div align="center">

  ## db/
  contains database file and model declarations

</div>

### db/database.py
defines the engine, creates the `SessionLocal` variable used throughout the api to instanciate db sessions and stage changes

### db/models/user.py
users model and table declaration
```
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.timezone("America/Sao_Paulo", func.now()),
        nullable=False,
    )
```
- [x] **TODO** implement the user model through the system

### db/models/vote.py
vote model and table declaration. currently used for calculating the `scores` dict
- [x] **TODO:** change timezone handling in created_at for librewolf users
```
class Vote(Base):
    __tablename__ = "votes"
    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    voter = relationship("User", foreign_keys=[voter_id])
    target_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    target = relationship("User", foreign_keys=[target_id])
    value = Column(Integer, nullable=False)
    reason = Column(Text)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.timezone("America/Sao_Paulo", func.now()),
        nullable=False,
    )
```


<div align="center">

  ## services/
  dfsdfsf

</div>

### services/auth.py
- defines the `sessions` dict, which is basically a list of `Users`associated with `session_id`s. 
- defines the `get_current_user` function, which returns a `user` model by querying the `user_id` inside the session_id
- [ ] **TODO:** (timeout) timeout vote weight modifier should be associated to a `session_id`

### services/render_service.py
- defines the `render_scoreboard` function.
  - takes the `scores` dict obtained from `score_service.py`, then runs a loop defining each row div for the scoreboard, wrapping it in the scorebard div, and returns that html.
  - [ ] *TODO:* change this to some sort of auto update (maybe in `pages.py`?). so that scoreboard changes without needing user input
  - [x] **TODO:** add last reason for vote in each row

### services/score_service.py
  stub for the scoring system.
  - currently just instanciates the `compute_scores` func which:
    - queries the `vote` and `user` rows from the db 
    - makes a `scores` dict by iterating through `users` and summing all the votes for each user in the `target_id` attribute of each vote
  - [ ] **TODO:** gotta think of a better data structure to compose the current scores. 
  - [ ] **TODO:** model for a scoring system where the score is a limited amount

### services/user_service.py
 - series of boilerplate queries to the db to more easily instanciate users.
 ```
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
 ```

<div align="center">

  ## services/
  contains the html jinja files that are returned by `api/pages.py`

</div>

--- 

<br>

<div align="center">

i hope it made sense to you, cos it doesnt make sense to me

</div>
