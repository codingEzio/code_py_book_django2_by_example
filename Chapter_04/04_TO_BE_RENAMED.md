
### Foreword 
- **Registration** is coming!

### Let's setup for it 
1. First we'll need user's info (therefore by using a *form* (i.e. ```forms.py```))
2. And the *logic* in the ```views.py``` (app-level)
3. the basic route on the ```urls.py``` (app-level)
4. and two templates (under ```templates/account/```)
    - ```register.html``` (display form)
    - ```register_done.html``` (welcome msg (optional))
5. add entries for needed places 
    - ```http://127.0.0.1:8000/account/login/```
        - display sth like "if you haven't registered, register here (show a link)" 
    - ```http://127.0.0.1:8000/account/register/``` (after submitted)
        - display sth like "ready to go" & "click here to log in"