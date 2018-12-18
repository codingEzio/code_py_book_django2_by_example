
### Here's what we're gonna do
- [x] add ```csrf_token``` for every templates we've created (keyword: ```auto```, ```AJAX```)
- [ ] new feature: ```like``` for users to "like an image"
- [ ] custom decorate (for views, powered by **AJAX**)
- [ ] pagination (also powered by **AJAX**)

------- 

### Auto add ```csrf_token``` ☺️
- Only one file need to be changed :D
- Make these changes to ```ROOT/app-account/templates/```**```base.html```**
    1. import ```.js``` 
    2. ...  ``` xhr.setRequestHeader("X-CSRFToken", csrftoken);```  ...

