### Starting **from this chapter**, we'll build 
1. An auth system for users to *register*, *log in*, *edit their profile*,  and *change*/*reset* their password.
2. A followers' system to allow users to follow each other.
3. A functionality to display shared imgs & implement a bookmarklet for users to share imgs from any website. 
4. An activity stream for each user that allows users to see the content uploaded by the people they follow.

### In **this** (i.e. 4th) chapter, 
- We'll build the **auth** parts (i.e. *register* & else).
- Here we go! 

------- 

### Getting started 
1. ```pip3 install Django==2.0.5```
2. ```django-admin startproject bookmarks .```
3. ```django-admin startapp account```
4. ```./manage.py migrate```

------ 

### Some notes here 
- We'll use the ```django.contrib.auth``` auth *framework* :P
    - it also got the essential parts, 
    - e.g. *models, views, forms* etc.
 - A new concept: ***Middleware*** (more notes'll be added later)

### Okay! How do we create the **logic view**?
- There should be something like 
    1. form: get username & password 
    2. auth: check it against the DB
    3. state: check the user is active or not 
    4. log the user into the website (& start an auth_ed session)
- Let's start 
    1. A form
        - ```forms.py```
            - two input filed, simple af, right?
    2. Logic & rendering 
        - Logic
            1. via ```GET```
                - blank form 
            2. via ```POST```
                - *POST* with input data 
                - Is it valid 
                    1. not valid 
                        - continue rendering (no more other stuff)
                    2. valid 
                        1. clean up the input 
                        2. check against the DB
                            1. got one (thus not ```None```)
                                - is it active  
                                    1. warning, deactivated account
                                    2. auth success!
                            2. nope (not exists)
                                - invalid login
        - Rendering 
            1. get the form by ```from .forms import LoginForm```
            2. render with *templates* 
    3. Templates (all under ```app-account/```)
        - base 
            - ```/templates/base.html```
        - css
            - ```/static/css/base.css``` (get it from [here](https://raw.githubusercontent.com/PacktPublishing/Django-2-by-Example/master/Chapter04/bookmarks/account/static/css/base.css))
        - login
            - ```/templates/account/login.html```
    4. Okay, now the ***```urls```*** !
        - proj level: ```proj-bookmarks/urls.py```
            - add ```path('account/', include('account.urls')),```
        - app level: ```account/urls.py```
            - add ```path('login/', views.user_login, name='login'),```
- Okay! Now you can test it 
    - go directly to [http://127.0.0.1:8000/account/login/](http://127.0.0.1:8000/account/login/)

-------- 

### 