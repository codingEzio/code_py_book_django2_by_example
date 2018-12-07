
### Type these cmds to get started 
- ```python
       from django.contrib.auth.models import User
       from blog.models import Post
        
       user = User.objects.get(username='alex')
    ```

### Quick tips
1. You can use **multiple DBs at a time**,<br>and program **DB routers** to create custom **routing schemes** <small>(specific app use specific DB)</small>.

### Demystifying the terms
- Here it is 
    
    | TERM | MY UNDERSTANDING | 
    | :--- | :----- | 
    | ```Managers``` | an object for managing the data was retrieved | 
    | ```QuerySet``` | simply **SELECT** in *SQL* | 
    | ```filter``` | e.g. **WHERE**, **LIMIT** in *SQL* | 


### Some guessing (to be clarified)
- Model's classname 🗣 Manager (Post.objects => Post.a_more_intuitive_name)
- MODEL_NAME.MANAGER.METHOD (e.g. Post.published.all())
- Rewriting the *Manager* is like *sub-query* for me. 