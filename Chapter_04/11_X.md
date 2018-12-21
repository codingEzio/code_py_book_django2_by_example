### This is Chapter 06, we'll cover these 
- [x] Create many-to-many relationships with an **intermediary model**
- [x] Build a **follower** system 
- [ ] Create an **activity stream** application 
- [ ] Add **generic relations** to models 
- [ ] Optimize ```QuerySets``` for related objects 
- [ ] Using ```signals``` for ?denormalizing counts 
- [ ] Store items in ***Redis***

----------

### Adding fields to ***app-account/***```models.py```
- New tables ```Contact```
    1. ```user_from```, ```user_to``` and one more ```following``` :D
    2. migrate it 
        - ```./manage.py makemigrations account```
        - ```./manage.py migrate```

### and views & routes (both under the app-account folder)
- ***views.py***
    - preparation
        - create some users () 
            - & upload respective avatars, do it at admin-page!
        - It seems that the *avatar* part is missing in the registration page...
    - notes 
        - We’re only adding two funcs: ```user_list``` (all users) & ```user_detail``` (one’s detail)
- ***urls.py***
    - add these 
        - ```path('users/', views.user_list, name='user_list'),```
        - ```path('user/<username>/', views.user_detail, name='user_detail'),```
    - then **get the absolute url**! 
        - This time we alter the **settings.py** (under proj-bookmark folder)
        - add the ```ABSOLUTE_URL_OVERRIDES = ...``` (go see the code for details)
### two more templates under ***app-account/templates/account/***
- first create a folder called ```user```
    - **list.html** 
    - **detail.html**
### finally 
- add an entry to the homepage! 
    - right here: ```app-account/templates/```**```base.html```**
- you can go to the homepage, click the nav ```People```, 
    - there’s should be a list of users with avatars (if not, create them)
        - users should be >= 2 
        - avatar also should be assigned 
    - and if you click the users’ avatar, you should be able to see
        - the user profile (avatar, name)
        - and the images he/she bookmarked 

----------

### Okay, now let’s make user could follow each other (by ***AJAX***)
- Only three files were included 🍺
    1. ```app-account/```**```urls.py```**
    2. ```app-account/```**```views.py```**
    3. ```app-account/templates/account/user```**```detail.html```**
- Okay, the ***urls.py***
    - simply add this: ```path('users/follow/', views.user_follow, name='user_follow'),``` 
    - do make sure put it **before** the ```path('user/<username>/', views.user_detail, ...)```                       
- Just sayin'
    - The ***views.py*** & the ***templates*** itself (& ***AJAX*** code inside) are *TIGHTLY CONNECTED*.
- These two (view, templ)
    - In brief, *jQuery* playin' with the json-response returned by *views*
    - Go see the ```image_like``` for more details (very similar to func we're writing now)
- Note
    - There're still ?*one* thing I haven't fully understand: *ManyToManyField* blabla..

