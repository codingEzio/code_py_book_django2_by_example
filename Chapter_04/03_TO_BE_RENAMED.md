
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
- 