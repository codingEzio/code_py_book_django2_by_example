
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