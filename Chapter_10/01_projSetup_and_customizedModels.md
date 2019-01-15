### Foreword
- We’ll build an ***e-learning platform*** plus this is the final project.
    - It allows instructors to **create courses** & **manage their contents**.
- Note
    - For those *weird* words, just go check **the aliases** previously defined.

### Basic setup
- one cmd for *install-then-add-requirements*
    - ```addreq: aliased to f() {  pip3 install $1 && pip freeze > requirements.txt && clear && bat requirements.txt; };f```
- aliases for Django commands
    - meta
        - ```alias djproj="django-admin startproject "``` <small>( **educa/educa/** )</small>
        - ```alias djapp="django-admin startapp "```
        - ```alias djma="python ./manage.py "```
    - non-meta
        - ```alias djnewadmin="./manage.py createsuperuser"```
        - ```alias djserve="./manage.py runserver "```
        - ```alias djmakemig="./manage.py makemigrations"```
        - ```alias djmig="./manage.py migrate "```
- aliases for some often-used cmds
    - ```alias fword="grep -rnw '.' -e "```
- modules
    - ```addreq Django==2.0.5```
    - ```addreq Pillow==5.1.0```
- skeleton <small>( the *order* matters )</small>
    - ```djproj educa && cd educa```
    - ```djapp courses```
    - ```djnewadmin``` <small>( create an user for later uses )</small>
    - ```courses.apps.CoursesConfig``` <small>( **educa/settings.py** :: ```INSTALLED_APPS``` )</small>

### Adding models
- Structure (e.g.)
    - Subject::Math
        1. Course::1st::PreCalculus
            1. Module::1st::Prerequisites
                - text, vid
            2. Module::2nd::Blabla
                - text, vid
        2. Course::2nd::Intro-Calculus
            1. Module::1st::Blabla
                - img, text, vid
            2. Module::2nd::Blabla
                - img, text, vid, files
- Structure as code <small>( **courses/models.py** )</small>
    1. ***```Subject```***
        - ```title```, ```slug```
    2. ***```Course```***
        - ```subject``` <small>( fk )</small>
        - ```title```, ```slug```
        - ```owner```, ```overview```, ```created```
    3. ***```Module```***
        - ```course``` <small>( fk )</small>
        - ```title```, ```description``` 
- Register it at backend <small>( **courses/admin.py** )</small>
    - Just go check the code :D 

### Adding sample data to models
- Hey, hey, hey!
    - You first need to **generate some data** <small>( at [admin page](http://localhost:8000/admin), of course )</small>.
    - You can start after you’ve added some data.
- Lemme explain the details
    - Cntrol its **scope** (all | specific)
        - ```courses``` 
        - ```courses.Subject``` 
    - Export
        1. **JSON** format by default.
        2. Print to **standard output** <small>( *terminal* )</small>.
        3. Use ```--indent``` to <small>( slightly )</small> control the format <small>( of JSON )</small>
    - Export path 
        - We’ll store it at *app-courses/* **fixtures/**.
        - While importing, it’ll also look up there first <small>( under each app )</small>.
    - More
        - Go check the doc, I’m just *using* it at the surface level.
        - Such as 
            1. [Providing initial data for models](https://docs.djangoproject.com/en/2.0/howto/initial-data/#initial-data-via-fixtures)
            2. [Fixture loading (testing tools)](https://docs.djangoproject.com/en/2.0/topics/testing/tools/#topics-testing-fixtures)
- You can run these cmds (under **root-educa/** ) 
    - ```djma dumpdata courses```
        - ```--indent=4```
        - ```--output=courses```**```/fixtures/```**```subjects.json```
    - ```djma loaddata subjects.json```
- Some stuff you need to notice
    - It’ll **overwrites** the stuff you’ve (added | modified) before.
    - It can be also used while you’re **writting tests**.

### Adding *missing* ```content```-related models
- Model ```Content```
    - part One: a foreign key pointing to the ```Module```
    - part Two: a **generic relation** to *associate any kind of content*.
- For the 2nd part, 
    - We'll created **different model** for *each type of content*.
        1. All content models'll have **some fields in common**.
        2. And they'll have its additional fields to **store custom data**.
    - Here we're gonna use the concept ***abstract models***
        1. We'll define a *base* model with attrs like ```owner```, ```title``` etc.
        2. Add the ```class Meta``` :: ```abstract = True``` to the *base* model
        3. Impl the four classes by inheriting the *base* model 
            - i.e. *Text*, *File*, *Image*, *Video* 
    - At last, make a little changes for model ```Content```
        - ```content_type = models.ForeignKey(.. , .. , NEW)```
        - ```NEW```
            - ```limit_choices_to = { .. : ('text', 'video', .. ) }```

### At last
- We need to let *modules*  & *contents* follow a particular **order**.
- Details are in the next section of this file.

-------- 

### Customizing fields 
- We could create our own model 
    - to store custom data
    - alter the behavior of existing fields 
- Ways to specify an order for objects is 
    - by adding a ```PositiveIntegerField``` to our models.
- What functionalities we'll build 
    - **Auto assign** an order value **when no specific order is provided**.
        - i.e. assigning the num comes after the last existing ordered obj
            - e.g. There're two objs with order ```1``` and ```2``` respectively
            - when saving the 3rd obj, it'd be auto assigned with an ```3```.
    - The objs should **be ordered with respect to other fields** 
        1. Course **modules** will be ordered with repsect to the **course**.
        2. Module **contents** will be ordered with respect to the **module**.
- Okay, make a new file **app-courses/fields.py**
    - I haven't fully understand how it works.
    - Here's a rough procedure for it:
        1. Inheriting ```models.PositiveIntegerField```
        2. ...

### Using the *customized* fields
- Edit **app-courses/models.py** <small>( import ```OrderField``` first )</small>
    - Add these to both: model ```Module``` & model ```Content```
        1. ```.. = OrderField(.. , for_fields=['LOWCASE_PAR_MODEL']```
        2. ```class Meta``` :: ```ordering = ['order']```
    - Migrate
        1. ```djmakemig courses``` <small>( **1**, **0**, **1**, **0** )</small>
        2. ```djmig```

### Now let's test it
- Still, first make sure you've got sample data at the backend!
- Here it is
    
    ```
        # The `User` & `Subject` is not that important
        from django.contrib.auth.models improt User
        from courses.models import Subject, Course, Module
        
        # The value depends
        usr = User.objects.last()     # 'alex'
        sbj = Subject.objects.last()  # 'S.E.'
        
        # Modules in one course
        c1 = Course.objects.create(subject=sbj,
                                   owner=usr,
                                   title='Course One',
                                   slug='course-one')
        c2 = Course.objects.create(subject=sbj,
                                   owner=usr,
                                   titlt='Course Two',
                                   slug='course-two')
                                   
        # These `order`s would be {0, 5, 6}
        c1m1 = Module.objects.create(course=c1, title='C1M1')
        c1m2 = Module.objects.create(course=c2, title='C1M2', order=5)
        c1m3 = Module.objects.create(course=c3, title='C1M3')
        
        c2m1 = Module.objects.create(course=c2, title='C2M1')
        assert c1m1.order == c2m1.order  # True
    ```
    