
### Foreword 
- We'll add new features, that's for sure.
- And we'll also rewrite parts of the program :P (e.g. ```auth```)

### Tips I need to say 
- The orders inside the ```INSTALLED_APPS``` **do matters** (```settings.py```) 

------ 

### Use Django's *logic* & *logout* 
- First, we need to modify the ```urls.py``` (app-account)
    1. comment out we've prevly written: ``` path('login/', views.user_login```
    2. import the views provided by Django
        - ```from django.contrib.auth import views as dj_auth_views```
        - ```path('login/', dj_auth_views.LoginView.as_view(), name='login'),```<br>```path('logout/', dj_auth_views.LogoutView.as_view(), name='logout'),```
- Now we'll need templates 
    1. create a folder under ```templates``` => ```templates/registration/```
        - This is the default path for the **auth templates** (you **could** change it of course)
    2. Two new files under it (**registration/**)
        - ```login.html```
            - we've written this before, but this one is much better :p
            - this folder (*registration*) and this file (*login*) are tightly connected with the ```urls.py```
                - what we're doing is actually (& barely) write the templates 
                - about the *logic*? we've **already imported** in the ```urls.py``` (app-level)
            - also, if you go to ```localhost:8000/account/login```
                - what u entered is actually **this** page (rather than the one we've written before!!!)
            - there's a ***hidden input*** (i.e. ```next```)
                - you could *give* a val to it in the ```address bar```
                - like ```localhost:8000/account/login/``` + ```?next=/admin/```
                    1. when you logged in, 
                    2. you'll be redirected to the ```admin``` page (just for example)
        - ```logged_out.html```
            - still like ```login.html```
            - the actually logic is already done by Django 
                - which the packages we imported in the ```urls.py```
                - we're simply *rewrite* the templates :P 