<div align="center">

# development notes for aura score

</div>

<br/>

---
    
# MAJOR NEXT STEPS :

- [ ] overhaul to vote page (new button + pop up layout instead of form)
- [ ] TIMEOUT for `\vote` based on `session_id`!!
- [ ] how to run the api from my machine and keep the cookies online on updates

- [x] proper hashed authentication in `auth.py` and `/login` POST
- [x] migrate `users` dict to proper `User` model
- [x] model and implement score computation to `score_service`

### notes:
(2026/05/14) - i think i might put a pause on the weight modellign....it seems a bit counter intuitive. maybe i should just leave the raw sums of votes for now and then make a more complex scoring feature instead of trying to guess how the user behavior will be like

--- 

# CURRENT ISSUES TO FIXLATER:
- [ ] if no one has voted for a specific user, `compute_service` does not account them in computing `scores` 
- [ ] add typehint to `service/` functions

<br/>

---

# devlog

(2026/05/14) - going to implement a proper authentication feature using `passlib[bcrypt]`.
to generate pwssd:
```
python -c "from passlib.hash import bcrypt; print(bcrypt.hash('passwordhere!!'))"
```
apparently bcrypt needs to be on v4.0.1 or earlier for this to work with the current passlib or smt.idk

preliminary system working!

damn im very confused now..... tried to add middleware thing but just made a mess.... need to review before refactoring:w

(2026/05/15) removed mess made by attempted session implementation. ok now. will do it properly.


---
---
