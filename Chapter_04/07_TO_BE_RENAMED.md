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