


### Type these cmds to get started 
- Here it is 
    
    ```
       from django.contrib.auth.models import User
       from blog.models import Post
        
       user = User.objects.get(username='alex')
    ```

### Quick tips
1. You can use **multiple DBs at a time**,<br>and program **DB routers** to create custom **routing schemes** <small>(specific app use specific DB)</small>.
2. Some concepts that I still <br>do not fully understand was stored as *bookmark* on **Dash** app <small>(this one is for myself)</small>.

### Demystifying the terms
- Here it is 
    
    | TERM | MY UNDERSTANDING | 
    | :--- | :----- | 
    | ```Managers``` | an object for managing the data was retrieved | 
    | ```QuerySet``` | simply **SELECT** in *SQL* | 
    | ```filter``` | e.g. **WHERE**, **LIMIT** in *SQL* | 

### Some guessing (to be clarified)
1. manager
    - Model's classname 🗣 Manager (Post.objects => Post.a_more_intuitive_name)
    - MODEL_NAME.MANAGER.METHOD (e.g. Post.published.all())
    - Rewriting the *Manager* is like *sub-query* for me. 
2. order
    - model => view => url (esp. variable part)