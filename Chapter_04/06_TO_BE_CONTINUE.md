
### Foreword
- Two things ahead: **add social auth** & **X** :P

-----

### Add social auth 
- Concept 
    - **Python Social Auth** is a module that *simplifies the process of adding social auth* :P
        - [Python Social Auth](https://github.com/python-social-auth)
        - [Python Social Auth documentation](https://python-social-auth.readthedocs.io/en/latest/intro.html)
- Preparation
    1. install by ```pip3 install social-auth-app-django==2.1.0```
        - add it ( i.e. ```'social_django'``` ) to ```INSTALLED_APPS``` (```settings.py```)
    2. now run ```./manage.py migrate```
        - then it'll appear on the backend (check it here: [localhost:8000/admin](http://localhost:8000/admin/))
    3. add them (*python-social-auth*) to ```urls.py```  (project-level)
        - which is ```path('social-auth/', include('social_django.urls', namespace='social')),```
    4. since some (social) services will not *allow* <br>the redirecting of users to ```127.0.0.1``` (or other stuff like this)
        - you **need some hack!** 
            1. add ```127.0.0.1 mysite.com``` to your ```/etc/hosts``` file 
            2. edit like ```ALLOWED_HOSTS = ['mysite.com', 'localhost', '127.0.0.1']``` (the ```settings.py```)
    5. now you could access it  by ```http://mysite.com:8000/account/login/```
        - we don't actually finished anything, yet :P
- Coding 
    - 
