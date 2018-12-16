### Foreword 
- This is **Chapter 05**
- We’ll actually finish the features (e.g. *bookmarklet*) we haven’t written, yet 🙃
- What will we do, exactly? (quotes)
    1. many-to-many relationships 
    2. using ```jQuery``` 
    3. using ```sorl-thumbnail``` (py-lib)
    4. custom *behavior* for ```forms```
    5. custom *decorators* for ```views``` 
    6. *AJAX* views & pagination 

---------- 

### Getting Started 
1. ```djangoadmin startapp images```
2. add ```images.app.ImagesConfig``` to ```INSTALLED_APPS``` (**settings.py**)

### What we're gonna do 
1. A ```model``` to store **images** & **their info** :P
2. A ```form``` & a ```view``` to handle **image uploads**
3. A system for users to be **able to post images** (that they find on external sites)

---------- 

### Let's write ```models```! (app-images)
- Needed fields 
    - ```user```, ```title```, ```image```
    - ```url```, ```slug```, ```created```
    -  ```description```, ```users_like_for_img```
- Override ```save()```
    - For the purpose of auto-generating the **```slug```** fields (which is based on **```title```**)
- Migrate (sync to DB)
    1. ```./manage.py makemigrations images```
    2. ```./manage.py migrate images```
- Register at ```admin.py``` (app-images)
    - Mainly how it was display at the backend 
    
    
### Okay, let's list the **TODO**s first! 
- [x] Side of *HTML*: ```forms.py```
    1. Provide a *hidden input* (for ```GET``` the image that is gonna be ```POST```ed later)
    2. Clean the url & check the extension (```.jpg | .jpeg``` only)
    3. Override the ```save()```
        - the attrs of the image 
        - ```request``` the image & make it ready for being stored to DB (```ContentFile```) 
- Sync to DB & rendering
    - [x] ```views.py```
        - Display form 
        - Save to DB (image itself & the one upload the image)
        - Rendering 
    - [x] ```create.html``` (templates)
        - Tree
            - **images/** -> **templates/images/image** -> ```create.html```
        - Steps 
            - One for ***get the url*** (of image) (well, in address bar ...)
            - One for ***post to DB*** (submit)
- Route stuff
    - [x] ```bookmarks/urls.py``` & ```images/urls.py``` (project | app)
        1. ```path('images/', include('images.urls', namespace='images')),```
        2. ```path('create/', views.image_create, name='create')```
            - Two things need to be done before adding the path :D
                1. ```from . import views```
                2. ```app_name = 'images'```
    
### Let's test it!
- Oh! You might (*well, definitely*) meet an error called ```AttributeError```
    - That's **OKAY** (cuz the image **WILL BE** saved)
    - The error was raised only cuz we haven't implement the ```get_absolute_url()```, ***yet***  
- And you might encounter a *403 Error* (mostly **network issues**)
    - Some site like [CelebMafia](https://www.celebmafia.com) will definitely meet this one!
    - From what I found (well, one site is enough for testin')
        1. [GotCeleb](http://www.gotceleb.com)
- Try it!
    - upload by (manually "POST" 🤣)
        - 127.0.0.1:8000/images/create/?title=**TITLE**&url=**URL**
    - check it by (backend side)
[localhost:8000/admin/images/image/](http://localhost:8000/admin/images/image/)