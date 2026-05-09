
<div align="center">

# development notes for aura score 

(commit e5b7580ab70442ee10419c9f41442c7745c3e15f)

</div>

---

# api/

### auth.py
- `/login` POST endpoint
  checks use and compares with password in the `users` dict. then assigns a session id to the username. returns a "bad login" html if password doesnt match. redirects to `/vote-page` if successful

### vote.py
- `/vote` POST endpoint
  does some validation (like if the current_user isnt the target user) and commits the new vote to the db. returns an instance of `render_scoreboard()` with the updated scores
  - [ ] *TODO:* change this to just return a change of states or smt. updates to `render_scoreboard()` should be managed by the render function

### pages.py
- `/login` GET endpoint
  - returns the login page jinja template. no context besides request.
- `/vote-page` GET endpoint
  - calculates `scores`,
  - queries `render_scoreboard(scores)` for the `scoreboard_html`,
  - runs through the `users` dict to get a list of voting `options`
  - then passes all as context to the index jinja template and returns it.
- `/` GET endpoint
  - calculates `scores`, 
  - queries `render_scoreboard(scores)` for the `scoreboard_html`,
  - then passes both as context to the index jinja template and returns it.


# core/

### users.py
currently just a dict with the users and passwords. temporary workaround until the users are properly migrated to db
- [ ] *TODO:* convert this to a mapping table using the user model

### templates.py
literally just:
```
def get_templates():
    return Jinja2Templates(directory="templates")
```
returns the templates defined in `templates/`


# db/
contains the database file

### database.py
defines the engine, creates the `SessionLocal` variable used throughout the api to instanciate db sessions and stage changes

### models/user.py
users model and table declaration, not implemented yet
- [ ] **TODO** implement the user model through the system

### models/vote.py
vote model and table declaration. currently used for calculating the `scores` dict

# services/

### auth.py
- defines the `sessions` dict
- defines the `get_current_user` function

### render_service.py
- defines the `render_scoreboard` function.
  - currently sorts the `users` dict (lol) in reverse order, then runs a loop defining each row div for the scoreboard, wrapping it in the scorebard div, and returning that

### score_service.py
  stub for the scoring system.
  - currently just instanciates the `compute_scores` func which:
    - takes the `votes` dict and `users` list.
    - makes a `scores` dict by iterating through `users` and summing all the votes for each user in the `target_id` attribute of each vote

# templates/
contains the html jinja files that are returned by `api/pages.py`

---

<br>

<div align="center">

this documentation is temp

</div>
