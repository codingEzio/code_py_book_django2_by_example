
### Now it's time to impl the ```password reset``` parts! 
- Just a reminder
    - A large portion of the **auth** part is based on Django :P
    - that means *most work could be done by modifying a little to the default views*

### Password change  
- ```urls.py``` (app-level)
    - one for *pwd-change*, one for *page-after-pwd-change*
        1. ```path('password_change/',dj_auth_views.PasswordChangeView.as_view(), name='password_change'),```
        2. ```path('password_change/done/', dj_auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),```
- two templates under ```app-folder/templates/registration/```   
    - these
        1. ```password_change_form.html```
        2. ```password_change_done.html```
    - now you could go [localhost:8000/account/password_change/](localhost:8000/account/password_change/)     
        - make sure that **you've logged in**, so you could see the right page 
        - also, it IS functional right now :P
    
### Password reset 
- There’re *five* templates (you can also call it ***scenarios*** 🤣)
    - first, you wanna reset ur pwd
        - link: account/password_reset/
        - name: ```password_reset_form.html```
    - second, the (reset) mail was send
        - link: account/password_reset/done/
        - name: ```password_reset_done.html```
    - and, you got the link from the terminal 
        - link: account/reset/MQ/523-dc0fff93ba5d6cf414da/
        - name: ```password_reset_email.html```
    - u clicked it and being brought to the reset page 
        - link: account/reset/MQ/set-password/
        - name: ```password_reset_confirm.html```
    - you’ve reset the pwd (successfully)
        - link: account/reset/done/
        - name: ```password_reset_complete.html```
- And the **email** (y’all need a reset email, right?)
    - ```EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'```
- Lastly, the ```urls.py``` (just glimpse)
    - ```password_reset/```
    - ```password_reset/done/```
    - ```reset/<uidb64>/<token>/```
    - ```reset/done/```
- One more, let’s add a link to the ```login.html``` 
    - it’s under the ```templates/registration/``` folder 
    - ``` ... href="{% url "password_reset" %}">Forgotten ur passwd? ... ```
    
------- 

### Foreword 
- **Registration** is coming!

### Let's setup for it 
1. First we'll need user's info (therefore by using a *form* (i.e. ```forms.py```))
2. And the *logic* in the ```views.py``` (app-level)
3. the basic route on the ```urls.py``` (app-level)
4. and two templates (under ```templates/account/```)
    - ```register.html``` (display form)
    - ```register_done.html``` (welcome msg (optional))
5. add entries for needed places 
    - ```http://127.0.0.1:8000/account/login/```
        - display sth like "if you haven't registered, register here (show a link)" 
    - ```http://127.0.0.1:8000/account/register/``` (after submitted)
        - display sth like "ready to go" & "click here to log in"