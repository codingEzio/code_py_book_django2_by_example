
### Foreword 
- We're gonna talk about ***extending the user model*** :P
- It's gonna be FUN!! 🤣

### Preparing stuff
- base model ```account/models.py```
    - a new class called ```Profile```
        1. a user
        2. birth date 
        3. photo (aka *avatar*)
- static stuff (**avatar** needed)
    - ```settings.py```
        - ```MEDIA_URL = '/media/'```
        - ```MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')```
    - ```bookmarks/urls.py```
        - sth like ```urlpatterns += static(settings.MEDIA_URL, ...)```
    - and a new module 
        - ```pip3 install Pillow=5.1.0```
- migrate it, please :P
    1. ``` ./manage.py makemigrations``` 
    2. ```./manage.py migrate```
- one more step, *registering* it inside the ```app-account/admin.py``` 
    - Just a glimpse: ```... ProfileAdmin ...``` (go see the code!)
- **Now** you should be able to see it at [localhost:8000/admin/account/profile/](http://localhost:8000/admin/account/profile/)
    - Also the avatars you uploaded will stored at the root folder (same level as proj | app)
    - of course it's bad practices, we'll just place it there for now, might fixing it later :P