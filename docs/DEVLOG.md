<div align="center">

# development notes for aura score

</div>

<br/>

---
    
# MAJOR NEXT STEPS :

- [ ] overhaul to vote page (new button + pop up layout instead of form)
- [ ] TIMEOUT for `\vote` based on `session_id`!!
- [x] how to run the api from my machine and keep the cookies online on updates

- [x] proper hashed authentication in `auth.py` and `/login` POST
- [x] migrate `users` dict to proper `User` model
- [x] model and implement score computation to `score_service`

### notes:
(2026/05/14) - i think i might put a pause on the weight modellign....it seems a bit counter intuitive. maybe i should just leave the raw sums of votes for now and then make a more complex scoring feature instead of trying to guess how the user behavior will be like

--- 

# CURRENT ISSUES TO FIXLATER:
- [ ] add vote_modal code to render_voting_scoreboard
- [ ] update docs!
- [ ] if no one has voted for a specific user, `compute_service` does not account them in computing `scores` 
- [ ] add typehint to `service/` functions
- [ ] add auth to `/admin` lol
- [x] add `<a>` back to index in vote page
- [ ] fix weird sql problem overflow thing

<br/>

---

# devlog

```
(2026/05/14) - going to implement a proper authentication feature using `passlib[bcrypt]`.
  to generate pwssd:
    python -c "from passlib.hash import bcrypt; print(bcrypt.hash('passwordhere!!'))"
  apparently bcrypt needs to be on v4.0.1 or earlier for this to work with the current passlib or smt.idk

  preliminary system working!

  damn im very confused now..... tried to add middleware thing but just made a mess.... need to review before refactoring:w

(2026/05/15) removed mess made by attempted session implementation. ok now. will do it properly.
  13:32 will start implementing proper session system now 
  13:46 will do it the stupid way and store sessions within the db
  14:15 implementing sessions in db... its kind of confusing now whenever we use `SessionLocal()` from the db. importing it as `UserSession`
  14:23 implemented. seems to work fine. i gotta test this by actually hosting it and accessing it from another machine now. i will work on this.
  14:50 it works! sessions now persist over reloads. gotta run `uvicorn with --host 0.0.0.0`

  15:25 will now start reworking the pages.
  17:08 styled pages and css. added new fonts
  18:06 remade render_scoreboard() with additional feats, made stub for render_voting_scoreboard() function
  which i'll use to make a vote modal window. to be done.

  ---
  
```

---
