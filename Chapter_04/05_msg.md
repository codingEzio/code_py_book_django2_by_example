
### Foreword
- Two things ahead: **message** framework & **custom auth backend** :P

-----

### Preparation for *message* part
- Basis 
    1. It is located at ```django.contrib.messages```
    2. Django has it by default (to us, it was pre-installed at ```startproject``` phase)
- Mechanics 
    - It was stored in a ***cookie*** by default (or ***session storage***), 
        - *and* they are displayed in the next request the user does.
        - it could both used in ```views.py``` and ```models.py```  (from the examples I've seen) 
    - My thought?
        - I think it's kinda like this: < raise-error THEN brought-to-frontend > 
        - Especially it got many types, e.g.
            - ```success()```, ```info()```
            - ```warning()```, ```error()```, ```debug()```

### Let's *do it*! (msg part)
- go directly to ```base.html```
    - there's a variable called ```messages```, where does it come from?
        - ```settings.py``` <br>-> ```TEMPLATES``` -> ```OPTIONS``` -> ```context_processors``` <br>-> ```'django.contrib.messages.context_processors.messages'```
- and the ```views.py``` (app-level)
    - just minor changes (display only)
        - saved successfully => ```message.success()```
        - raised error for it => ```message.error()```
- now you could go [localhost:8000/account/edit/](http://127.0.0.1:8000/account/edit/) to test it 