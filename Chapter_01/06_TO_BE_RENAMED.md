
### Foreword 
- We'll add **sitemap** for our site :P 

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
    - 