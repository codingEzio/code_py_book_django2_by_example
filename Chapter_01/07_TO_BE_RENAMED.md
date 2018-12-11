
### TOC of adding new feature (***full-text search***)  
- setup of PostgreSQL
- 

---------- 

### Setup of **PostgreSQL**
- For **macOS** 
    1. ```brew install postgresql``` 
    2. ```brew services restart postgresql```
    3. ```rm -fv /usr/local/var/postgres/postmaster.id``` (just in case)
    4. ```createuser -dP blog``` 
        - type ```psql``` -> ```\password blog``` to reset pwd if u want 
    5. ```createdb -E utf8 -U blog blog``` (the latter is DB's name)
- Oh, the "*driver*"! 
    - ```pip3 install psycopg2==2.7.4```
    - There's warning while I'm installing it 
        - UserWarning: The psycopg2 wheel package will be renamed from release 2.8; 
        - in order to keep installing from binary please use ```pip install psycopg2-binary``` instead. 
        - For details see: [initd.org/psycopg/docs/install.html#binary-install-from-pypi](http://initd.org/psycopg/docs/install.html#binary-install-from-pypi).
    - We ?can just ignore it for now :)
    
### And we need to modify the ```settings.py```
1. Here: ```DATABASES``` -> ```'default'```
    - ```python
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'blog',
        'USER': 'blog',
        'PASSWORD': sensitive.psql_db_password,
        ```
2. Then, we'll need to ```./manage.py migrate``` 
    - and run this: **```./manage.py createsuperuser``**. 
3. well, now we got a clean DB 
    - yet with no data 
    - just go ```http://127.0.0.1:8000/admin/``` to **gen some content**! (six posts is enough :P)
    
---------- 

### Base  
- ```settings.py```
    - ```INSTALLED_APPS```
        - ```django.contrib.postgres``` 

- related files (all under the ```PROJECT/app-blog```)
    - ```forms.py```
    - ```views.py```
    - ```urls.py```

- what does the three files do?
    1. a basic text field 
    2. logic & rendering  (also have ```PostgreSQL``` as backend)
    3. a decent url for access 

### So, now we got a (working?) simple ‘full-text search’ features!
- Go to [http://127.0.0.1:8000/blog/search/](http://127.0.0.1:8000/blog/search/)
- Not takin’ too much notes for now ( ***might added later?*** )