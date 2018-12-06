
### Note
- Some dead-simple basics won't be mentioned :P 

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