
### Foreword
- Two things ahead: **message** framework & **custom auth backend** :P

-----

### Preparation for *message* part
- Basis 
    1. It is located at ```django.contrib.messages```
    2. Django has it by default (to us, it was pre-installed at ```startproject``` phase)
- Mechanics 
    - It was stored in a ***cookie*** by default (or ***session storage***), 
        - *and* they are displayed in the next request the user does.
        - it could both used in ```views.py``` and ```models.py```  (from the examples I've seen) 
    - My thought?
        - I think it's kinda like this: < raise-error THEN brought-to-frontend > 
        - Especially it got many types, e.g.
            - ```success()```, ```info()```
            - ```warning()```, ```error()```, ```debug()```

### Let's *do it*! (msg part)
- go directly to ```base.html```
    - there's a variable called ```messages```, where does it come from?
        - ```settings.py``` <br>-> ```TEMPLATES``` -> ```OPTIONS``` -> ```context_processors``` <br>-> ```'django.contrib.messages.context_processors.messages'```
- and the ```views.py``` (app-level)
    - just minor changes (display only)
        - saved successfully => ```message.success()```
        - raised error for it => ```message.error()```
- now you could go [localhost:8000/account/edit/](http://127.0.0.1:8000/account/edit/) to test it 

----- 

### Now it's "*building a custom auth backend*"
- ***Intro***
    - The backend was defined by setting ```AUTHENTICATION_BACKENDS```
        - The default one is ```django.contrib.auth.backends.ModelBackend``` :P 
    - An auth backend is *a class that provides these two methods*:
        1. ```authenticate()```
            - Takes the ```request``` object & user credentials as params :P
            - and it returns ```user``` object match those stuff (if false => ```None```)
        2. ```get_user()```
            - Takes a user ID => return a ```user``` object 
- ***Start to customize it***
    - A new file under ```app-account```: 
        - intro
            - file: ```authentication.py```
            - class: ```EmailAuthBackend```
        - detail
            - simply rewriting those two functions 
            - aka ```authenticate()``` and ```get_user()```
    - Two values under ```settings.py```
        - ```python
             AUTHENTICATION_BACKENDS = [
                  'django.contrib.auth.backends.ModelBackend',
                  'account.authentication.EmailAuthBackend',
            ]
            ```
        - Oh! The orders for the values inside the ```AUTHENTICATION_BACKENDS``` **DO matters**!
            - If the 1st one is okay to go, then it'll stop there :P
    - Now you could still **log in** just like before,
        - the only (which is big) difference 
        - is that you **CAN** login either with *username* OR *email addr* 😌