
### Before the end of the Chapter 05
- [x] we’ll add the ```pagination``` (powered by **AJAX**)
- [ ] detailed notes for this part (***paging***)


------- 

### HowTo
- Two templates under ```app-images/templates/images/image```
    - **list.html**
    - **list_ajax.html**
- Two new changes under ```app-images/```
    - ***views.py***
        - ```def image_list()```
    - ***urls.py***
        - ```path('', views.image_list, name='list'),```
- One more changes in ```app-account/templates```**```base.html```**
    - OLD: ```<a href="#">Images</a>```
    - NEW: ```<a href="{% url "images:list" %}">Images</a>```