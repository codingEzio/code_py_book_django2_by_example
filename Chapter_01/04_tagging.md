
### A little tip 
- The ```<int:post_list>``` means 
    - convert the ```post_list``` to ```int``` type 
    - here's another example: ```<slug:tag_slug>``` :P 

### Foreword 
- what 
    - We'll add the *tagging* functionality 
- setup
    1. ```pip3 install django_taggit==0.22.2```
    2. modify ```settings.py```
        1. add ```"taggit"``` to **```INSTALLED_APPS```**
    3. modify ```models.py```
        1. ```from taggit.managers import TaggableManager```
        2. ```tags = TaggableManager()``` to ```class Post```
    4. migrate 
        1. ```./manage.py makemigrations blog```
        2. ```./manage.py migrate```
