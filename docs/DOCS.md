
<div align="center">

# development notes for aura score 

(commit e5b7580ab70442ee10419c9f41442c7745c3e15f)

</div>

---

# api/
endpoints go here

### api/auth.py
- `/login` POST endpoint
  checks use and compares with password in the `users` dict. then assigns a session id to the username. returns a "bad login" html if password doesnt match. redirects to `/vote-page` if successful

### api/vote.py
- `/vote` POST endpoint
  does some validation (like if the current_user isnt the target user) and commits the new vote to the db. returns an instance of `render_scoreboard()` with the updated scores
  - [ ] *TODO:* change this to just return a change of states or smt. updates to `render_scoreboard()` should be managed by the render function
  - [ ] *TODO:* update endpoint to accept vote reason
  - [ ] *TODO:* add timeout service to this endpoint! prevent spam

### api/pages.py
- `/login` GET endpoint
  - returns the login page jinja template. no context besides request.
- `/vote-page` GET endpoint
  - calculates `scores`,
  - queries `render_scoreboard(scores)` for the `scoreboard_html`,
  - runs through the `users` dict to get a list of voting `options`
  - then passes all as context to the index jinja template and returns it.
  - [ ] *TODO:* add vote reason text box
  - [ ] *TODO:* replace form with a button and pop up input box to register vote 
  - [ ] *TODO:* update to use new user model instead of `users` dict
  - [ ] *TODO:* (maybe) add a timeout element to page
- `/` GET endpoint
  - calculates `scores`, 
  - queries `render_scoreboard(scores)` for the `scoreboard_html`,
  - then passes both as context to the index jinja template and returns it.


# core/

### core/users.py
currently just a dict with the users and passwords. temporary workaround until the users are properly migrated to db
- [ ] *TODO:* convert this to a mapping table using the user model

### core/templates.py
literally just:
```
def get_templates():
    return Jinja2Templates(directory="templates")
```
returns the templates defined in `templates/`


# db/
contains the database file and models

### db/database.py
defines the engine, creates the `SessionLocal` variable used throughout the api to instanciate db sessions and stage changes

### db/models/user.py
users model and table declaration, not implemented yet
- [ ] **TODO** implement the user model through the system

### db/models/vote.py
vote model and table declaration. currently used for calculating the `scores` dict

# services/

### services/auth.py
- defines the `sessions` dict
- defines the `get_current_user` function

### services/render_service.py
- defines the `render_scoreboard` function.
  - currently sorts the `users` dict (lol) in reverse order, then runs a loop defining each row div for the scoreboard, wrapping it in the scorebard div, and returning that
  - [ ] *TODO:* change this to some sort of auto update (maybe in `pages.py`?). so that scoreboard changes without needing user input

### services/score_service.py
  stub for the scoring system.
  - currently just instanciates the `compute_scores` func which:
    - takes the `votes` dict and `users` list.
    - makes a `scores` dict by iterating through `users` and summing all the votes for each user in the `target_id` attribute of each vote

# templates/
contains the html jinja files that are returned by `api/pages.py`

--- 

# ideas/mayybe
### vote history page 
- show target vote history (reason, voters, etc)
- show voter vote history (same)

### alt score tab
- alternate scoreboard for non-voter users

---

<br>

<div align="center">

this documentation is temp

</div>
