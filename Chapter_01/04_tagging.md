
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
        
### Let the ***tag*** SHINE 😂 ! (**display-only**)
- Type ```./manage.py shell``` (shell-of-Django)
    - ```python
        from blog.models import Post
 
        post = Post.objects.get(id=1)
 
        post.tags.add('tech', 'music')
        post.tags.remove('music')
        
        post.tags.all()
        ```
- Now you **could** go check the admin-page 
    - You'd be able to see the effect of ***tag*** & its related posts :P 
- Okay! Now let's edit the ```list.html``` for **displaying**! 
    - Add after the title ```<h2> ... </h2>```
        - ```<p class="tags">Tags: {{ post.tags.all | join:", " }}</p>```
        
### Diving in! (list **all posts tagged with a specific tag**)
- modify ```post_list``` related things 
    - ```views.py```
    - ```urls.py``` 
- then its templates file 
    - ```list.html```
    
    
----------
    
### Now let's retrieving posts by ***similarity*** 
- < ***same ID means similarity, at least in here*** > 
- Lemme get a todo-list first 😇 
    - [x] retrieve all tags fro the current post 
    - [x] get all posts that are tagged with any of those tags 
    - [x] exclude the current post from the recommended posts 
    - [x] order the results by the num of tags shared with the current post 
    - [x] in case 2+ posts with the same num of tags, recommended the most recent one 
    - [x] limit the query to the number of posts we want to recommended 
- Only two files were related 
    - ```views.py```
    - ```detail.html```
- Simply a chain (kinda correspond to the code!)
    1. tag ID of the current post 
    2. get its related posts (not include itself)
    3. limiting the number of recommended posts 
    4. rendering (& passed to templates as vars) it 
    5. iterating it in templates (& get its own "absolute url", so u can click it)