
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