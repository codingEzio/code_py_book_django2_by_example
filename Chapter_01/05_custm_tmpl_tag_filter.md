
### Foreword 
- The era of **Chapter 3 BEGINS**!
- We'll **customize** our own **template tags** to ***perform custom actions*** :P 

----- 

### Setup 
- File
    - Structure 
        - blog/```templatetags/```
        - blog/**templatetags**/```__init__.py```
        - blog/**templatetags**/```blog_tags.py```
    - Note 
        1. the filename determines how you ref them in template (e.g. ```{% load blog_tags %}```)
        2. the tag name could be customized 
            - ```@register.simple_tag()                =>  it would use the func being decoed```
            - ```@register.simple_tag(name=TAG_NAME)   =>  it would use the TAG_NAME```
- Methods 
    1. ```simple_tag```: process the data and returns a string 
    2. ```inclusion_tag```: process the data and returns a **rendered** template
- Okay, let's edit the ```base.html``` (dead simple), 
    1. "import" by ```{% load blog_tags %}``` (put this before ```<!DOCTYPE html>```)
    2. use it by ```I've written {% my_post_count %} posts for now 😌.```
    
### Alright, let's add another feature: ***displaying latest posts in the sidebar*** 
- Still editing the blog/**templatetags**/```blog_tags.py```
    - A new function ```show_latest_posts()``` which is *decorated* by ```@register.inclusion_tag(...)```
- And the related two templates 
    - One for our purpose ```base.html``` (that make it displayed on the homepage)
    - And the func which is tightly connected with: **templates/blog/post/** ```latest_posts.html```

# And of course, ***most commended posts*** 🙂
- Still editing the blog/**templatetags**/```blog_tags.py```
    - A new function ```get_most_commented_posts()``` which is *decorated* by ```@register.simple_tag```
- And go on editing the ```base.html```
    - It's simply using the vals of variables that comes from the function we've written before :P

-----------

### Okay, new stuff is coming! 
- We'll **customize** our own **template filters** :P 
- What is it? Here's an example 
    > ```{{ post.body | truncatewords:30 | linebreaks }}```

### More examples 
- ```{{ variable | my_filter``` ```:"foo"```
- ```{{ variable | my_filter | another_filter ```
 
### Setup
- Add **markdown** support by 
    1. install by ```pip3 install Markdown==2.6.11```
    2. export dep by ```pip freeze > requirements.txt```
- And let's (continue) editing the ```blog_tags.py``` 
    - import 
        1. ```from django.utils.safestring import mark_safe```
        2. ```import markdown```
    - use it 
        ```@register.filter(name='markdown')```
        ```def markdown_format(...): ...```
    - ***DO see the code for more details***! 
- Ok, now let's modify the **templates**. 
    - ```detail.html```
        1. load by ```{% load blog_tags %}```
        2. replace: ```{{ post.body | markdown }}```
            - ```{{ post.body | linebreaks }}```
    - ```list.html```
        1. load by ```{% load blog_tags %}```
        2. replace: ```{{ post.body | markdown | truncatewords_html:30 }}```
            - old: ```{{ post.body | truncatewords:30 | linebreaks }}```