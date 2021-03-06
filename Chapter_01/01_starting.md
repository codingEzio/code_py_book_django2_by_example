
### Note
- Some dead-simple basics won't be mentioned :P 
- Not clear about it? ***READ THE FUCKING DOC***! 

### Setup only 
- ```django-admin startproject mysite .```
- ```./manage.py startapp blog```

### Getting started 
- ```./manage.py migrate``` (do run this in the very start)
    - By applying migrations, the **tables** for the initial apps **are created**.
- ```./manage.py runserver localhost:PORT``` 
    - You could specific the params for running (**DEBUG** use only)
    - In real world uses, you should pick one of these
        1. Apache
        2. Gunicorn
        3. uWSGI

### About project's **settings.py** (several of them will be mentioned)
- ```DEBUG```
    - Just remember to turn it off when go production. 
    - Also, this option'll affect other options (when in debug, xx not applies)
- ```ALLOWED_HOSTS```
    - ***Not applied when the debug mode is on***.
    - This option is specifically for production uses.
- ```ROOT_URLCONF```
    - The root url patterns for your application. 
    
### Terms 
- Project & applications 
    > Your can think of the *project* as ur website, <br>which contains several *apps* such as a blog, wiki etc.
    
### About the apps folder 
- ```admin.py```
    - where u **register** the *db models* to **include them in the (django's) admin site**. 
- ```apps.py```
    - the main conf of the *blog* app (well, I seldom touched this file before)
- ```migrations/```
    - contains *db migrations of ur app*. 
    - it allows Django *track ur model changes* => *sync the db accordingly* 
- ```models.py```
    - each app *need to have one*, while this file *could be left empty* 
- ```views.py```
    - receive -> process -> return 
    
### Let's design the schema for the 'blog' app
- Apparently, we need to write the ```models.py``` of related apps. 
- After we've finished, we need to **migrate** it. 
    1. first let Django knows ur app (**INSTALLED_APPS** in **settings.py**)
    2. then the ```makemigrates``` would applies for **all apps listed in it** <small>(*INSTALLED_APPS*)</small>
- About the *migrating* (example)
    - make it by ```./manage.py makemigrations blog```
    - check sql by ```./manage.py``` **```sqlmigrate```** ```blog 0001``` (not exec)
    - do migrate by ```./manage.py migrate```
- One last step, we need to **see** this at frontend (at least in *admin*!)
    - Edit **blog/admin.py**
        1. import models: ```from .models import Post```
        2. register to admin: ```admin.site.register(Post)``` (this'll be refactored soon)
        
### Customizing our admin model
- Just go see the ```blog/admin.py``` (lots of notes in there!)

-----------

### Here comes the **View** part (func-based)
- Simply put, 
    - A view is just *a function receives a request* then *returns a web response*.
    - All **the logic to return** the *desired* response goes inside the view. 
- One photo for current status (displaying post-list & indiv-post)
    - <img src="../img/img_chapter_01/0001_procedure.jpg" width=50% height=50%>
    
### Here comes the *another* one (class-based)
- Some good features for it 
    1. Organizing code related to specific kinds of methods (e.g ```GET```, ```POST```). 
    2. Using multiple inheritance to create **reusable classes** (aka **Mixins**). 
    3. ***Writing less code*** 😅
- So.. the old codes will be *rewritten using new ways*! 
    
    | FILE | CHANGE | ELSE | 
    | :--- | :--- | :---- | 
    | ```blog/views.py``` | *a new class* | with other class being imported |
    | ```blog/urls.py``` | *a new route* | old being commented out |
    | ```list.html``` | *change the paginator's obj name* | in the templates folder |