
### Add **sitemap** for our site :P 
- Aha

----- 

### Setup
- add it (Django got this!)
    - edit ```settings.py```
        - add line: ```SITE_ID = 1```
        - add apps (**INSTALLED_APPS**)
            - ```'django.contrib.sites',```
            - ```’django.contrib.sitemaps',```
- cuz there’s a new app, 
    - so you need migrate! 
        - ya need to do it every time you add a new app
    - since it’s built-in, not our model
        - so it’s just one cmd: ```./manage.py migrate```
        
### And the file
- **app-blog/**```sitemaps.py``` 
    - Well, we’re simply does these 
        - inherit the ```django.contrib.sitemaps.Sitemap```
        - and override some attrs, e.g. 
            - ```changefreq = 'weekly'```
            - ```def lastmod(self, obj): ...```
- **proj/**```urls.py``` (details are inside the code!)

### Now you can test it! 
- Go ```http://127.0.0.1:8000/sitemap.xml``` (simple af, right?)
- Oh! Be sure to change the **domain name**! 
    - which the default is ```example.com```
        - go ```http://localhost:8000/admin/sites/site/```
        - change to your own name (for me, it's ```localhost:8000```)
- then it'll generate the correct URLs (*sitemap.xml*)

----------

### Now let's create *feeds* for our blog posts 
- One word is enough: ***RSS***.

### Setup 
- app-blog/```feeds.py```
    1. get data, or get parts of data
    2. assign to specific vals, 
        - e.g. the ```item_title``` was for the titles in RSS
- app-blog/```urls.py```
    1. point to that url 
    2. provide a name for templates uses 
- templates/```base.html```
    - add ```<p><a href="{% url "blog:post_feed" %}">Subscribe by RSS</a></p>```
    
