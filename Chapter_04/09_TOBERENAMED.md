
### Here's what we're gonna do
- [x] add ```csrf_token``` for every templates we've created (keyword: ```auto```, ```AJAX```)
- [ ] new feature: ```like``` for users to "like an image"
- [ ] custom decorate (for views, powered by **AJAX**)
- [ ] pagination (also powered by **AJAX**)

------- 

### Auto add ```csrf_token``` ☺️
- Only one file need to be changed :D
- Make these changes to ```ROOT/app-account/templates/```**```base.html```**
    1. import ```.js``` 
    2. ...  ``` xhr.setRequestHeader("X-CSRFToken", csrftoken);```  ...

### Make users being able to ```Like``` an image
- Foreword 
    - Actually there’s only ***one*** shit to impl ... aka. the ```Like``` button 
    - It *simply* does two things 
        - Like / Unlike (text | HTML)
        - Like / Unlike (attr | Database)
- Some notes here 
    - Do remember it’s just *logic* & *get data* (it’s **programming**, not **magic**!)
    - Part of the **notes were taken inside the respective files** (do go see it!)
- Also ... 
    - Anything you’re *NOT* familiar with ... either ```AJAX``` or ```jQuery``` or ```Django``` etc. 
    - It ***HAS TO BE*** one of them 😅 
        - so ... it’s just *something to learn*, not something *cannot be overcame* 🤪
- Talkin’ the file structure
    - Well, some work has been done before (inside **base.html**) 
    - **app-image/urls.py**
        - route stuff: ```path('like/', views.image_like, name='like’),``` 
        - well, we won’t browser it directly (***later we’ll impl a deco to forbidden this operation!***)
    - **app-image/views.py**
    - **app-image/templates/images/image/detail.html**
- For ***views.py*** 
    1. get the ```id``` (DB) and the ```action``` (```like``` | ```unlike```, from js side)
    2. if you get those two vals (successfully), it’ll start to 
        - **get the image id** 
        - **get the action** (then ```add``` / ```remove``` the likes)
        - and **return a JsonRespose**
            - this one is **just** one more ```if``` in js side 
            - a glimpse here: ```if (data['status'] == 'ok')```
- ***detail.html*** :: templates part 
    1. first we get the users (whom like the current image)
        - ```users_like=image.users_like_for_img.all```
    2. the attrs in ```<a x=y x=y x=y>```
        - in concept
            - assign the vals we need (which’ll be given to ***AJAX***)
        - in reality 
            - ```data-*``` it belongs to *jQuery* stuff :)
            - it’s kinda like args for the ```{% block domready %}```
    3. the texts in ```<a x=y x=y x=y>``` 
        - notes 
            - it does **NOT** dup with the *AJAX* part 
            - which I thought it was (🤨, which is not, lol)
        - cases
            - you havn’t like it? => display ```like```
            - you liked it before => display ```unlike```
- ***detail.html*** :: ajax part (at the bottom, XD)
    - just go check the code! 
    - it ain’t good if just looking the words (not along with code)
- ***views.py***
    - ```ajax``` send the opt 
    - ```views``` receive it & process