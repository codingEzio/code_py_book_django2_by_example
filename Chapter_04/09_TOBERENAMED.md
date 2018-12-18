
### Here's what we're gonna do
- [x] add ```csrf_token``` for every templates we've created 
    1. *automatically*
    2. using ```AJAX```
- [ ] add a feature ```like``` for users to "like an image"

------- 

### auto-add ```csrf_token``` automatically 
- Only one file need to be changed :D
- Make these changes to ```ROOT/app-account/templates/```**```base.html```**
    1. import ```.js``` 
    2. ...  ``` xhr.setRequestHeader("X-CSRFToken", csrftoken);```  ...