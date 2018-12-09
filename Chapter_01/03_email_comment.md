
### Foreword 
- The era of **Chapter 2 BEGINS**!
- The first thing is **allow users to share posts** by *sending them emails* :P
- And after that, we’ll create a **comment system**.

----- 

### Sharing post by sending an email 😎
- Creating the ***forms*** (static thing)
    - app-folder/```forms.py```
        - inherit ```django.forms.Form```
        - create field (which’ll be conv to widgets of HTML)
- Importing it into ```views.py``` (real functionality)
    - firstly  
        - import form ```from .forms import EmailPostForm```
        - import get-post ```from django.shortcuts import get_object_or_404```
    - a new func ```post_share```
        - what does it do?
            - It mostly appears at each post (*detail page*)
            - So, it’s just a link (in users’ perspective)
        - what does it contain?
            - get object (current post)
            - send email or not 
                - via ```GET``` => display blank form (to be typed in)
                - via ```POST``` => post it 
                    - valid => ***send it then rendering the page***
                    - no? => Django (& browser) would stop
            - the email info 
                - content you’re gonna send (*subject*, *msg* etc. )
    - And the templates 
        - each post got a share link! (aka blog/post/```detail.html```)
        - share page itself (aka blog/post/```share.html```)
            - sent successfully 
            - OR display the sent-email page 
    - The blog/```urls.py```
        - A new (& valid) page for sending emails (ya need a page to display the forms! did you forget?)
    - The my_site/```settings.py```
        - configure the backend (whether it’s a real one or not)

### And let’s create the bloody 😙 comment system! 
- Actually I don't like the word '*system*' much, we'll use it anyway 😷 
- Let's follow the todo list :P 
    1. [x] a new model for saving comments 
    2. [x] a form to submit & validate the input 
    3. [x] a view that process the form & save the comment to DB 
    4. [x] edit the template to display the comments & the form (post_detail)
- Modifying the ```models.py``` first XD
    - Write it (details were inside the code!)
    - Make migrations (sync -> DB)
        1. ```./manage.py makemigrations blog```
        2. ```./manage.py migrate``` 
- And edit the ```admin.py``` 
    - which enables it being displayed on the admin page (better control)
- And the ```forms.py```
    - we'll use the *forms* **from the ```models.py```**
- And the ```views.py```
    - import 
        - **Comment** in ```models.py```
        - **CommentForm** in ```forms.py```
    - edit the ```post_detail``` (where *comment* should appear)
        - do the right thing for ```POST```, ```GET```
        - query the data (for templates using it)
        - display the form (comment)
    - Oh! There's one line you might be interested 
        - The ```post.comments.filter(active=True)``` line
        - that indicates if you change the state of ```active``` in admin (or DB)
            - the comments are (sort of) deleted (or sayin' 😏 "filtered out" )
- And the template: ```detail.html```
    1. how many posts (display as "N comments")
    2. comment concent (display as "Nth, By who, when & content itself")
    3. comment-form OR info (display as "form" OR "ur xx has been added")