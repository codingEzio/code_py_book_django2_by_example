
### Foreword 
- This is how our users would use it (either one)
    - Store ur link as bookmark & user click it on a webpage 
    - then the code would be exec-ed (i.e. then it'll *scrape* the pic!)

----------

### Basic setup 
- Foreword 
    - Most of this part (for now) is doing *js stuff* :D
- Here's what we're gonna do 
    - [x] add an entry (store the link) to the homepage 
        - Here ```app-account/templates/account/```**```dashboard.html```**
    - [x] a launcher of the core js 
        - it was stored at ```app-images/templates/```**```bookmarklet_launcher.js```**
    - [x] the core js file 
        - [x] the css along with it (how it was displayed (keyword:```jQuery``` ))
        - they were stored at here (under ```app-images/```**```static```**)
            - js: ```/js/bookmarklet.js``` (type it manually)
            - css: ```/css/bookmarklet.css``` (get it from [here](https://github.com/PacktPublishing/Django-2-by-Example/blob/master/Chapter05/bookmarks/images/static/css/bookmarklet.css) (directly copy it))
            
### And, what's more ...
- The *local server* (aka. ```localhost```) will meet **most of our needs**, 
    - there's still restrictions (& cannot be "*hacked*")
    - that's what [*ngrok*](https://ngrok.com/) is trying to accomplish :D
- Set it up
    1. Register at [ngrok.com](https://ngrok.com/]
    2. Download it to ```/usr/local/bin``` & run ```ngrok authtoken YOUR_AUTH_TOKEN```
    3. And one more: ```ngrok http 8000```
- Now, it's time to make some changes about ur code 😅
    - Edit ```ALLOWED_HOSTS``` in **settings.py**
        - append the ```THIS_ONE_VARIES.ngrok.io```
    - Modify ```bookmarklet_launcher.js``` & ```bookmarklet.js```
        - OLD: ```http://127.0.0.1:8000/```
        - NEW: ```https://THIS_ONE_VARIES.ngrok.io/```
    - Also, do make sure to change the url of the bookmark!!!
        - Still replacing the ```This_one_varis``` (every time u run the ```ngrok http 8000```)
- Note
    - For now, you could replace all the urls with the new url (while testing)
- Okay, you could test it now
    1. first save it as a bookmark (copy the js code as the url of the bookmark)
    2. go to a random site *then* click the bookmark (js code)
    3. it should be a simple UI for the images for the current page (not fully impl yet)
    
### We let js do some of the stuff for us 
- ```javascript
    jQuery('#bookmarklet').hide();

    window.open(site_url + 'images/create/?url='
        + encodeURIComponent(selected_image)
        + '&title='
        + encodeURIComponent(jQuery('title').text()),
        + '_blank'
    );
    ```

### The page that users'll be redirected 
- We still would encouter the ```AttributeError```, but ***that's OK***!
- Now let's impl the page (& logic) after users clicked the ```bookmark it```
- files-gonna-be-changed
    1. ```get_absolute_url``` in **models.py**
    2. the page that user'll be redirected to: ```templates/images/image/detail.html```
    3. get the pic 
        - route: ```images/urls.py```
        - render: ```images/views.py``` 
- actual-procedures
    1. add route (**urls.py**)
        - ```path('detail/<int:id>/<slug:slug>/',views.image_detail, name='detail'),```
    2. complete *models.py*
        - override ```get_absolute_url``` by ```reverse('images:detail', args=[self.id, self.slug])```
    3. use *views.py* to get the object & rendering 
    4. & and the templates 
    
    
----------


### Generating thumbnails 
- basic setup
    1. ```pip3 install sorl-thumbnail==12.4.1```
    2. add ```'sorl.thumbnail',``` to ```INSTALLED_APPS``` 
    3. migrate ```./manage.py migrate```
- make changes to ```templates/images/image/detail.html```
    - First, you got two ways to use it: ```{% thumbnail %}``` tag, or using a *custom* *```ImageField```*
        - We'll use the *tag* ways :D
    - okay, let's start 
        1. load it by ```load thumbnail```
        2. replace stuff
            - OLD: ```... {{ image.image.url }} ...```
            - NEW: ```{% thumbnail image.image "300" as img %}``` ... ```{% endthumbnail %}```
- note:
    - this one is completely optional :)
    - here's some [examples](https://sorl-thumbnail.readthedocs.io/en/latest/examples.html?highlight=imagefield) (from ```sorl-thumbnail```'s official tutorial)
    