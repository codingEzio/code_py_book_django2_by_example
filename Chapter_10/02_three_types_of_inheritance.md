### Raw thoughts about ```GenericForeignKey```
- ForeignKey: *normal* => *generic*, XD.
- Ah, I might need a much more comprehensive example ...

### Model inheritance :: *Abstract models*
- Features
    1. Put some common info into several models.
    2. No DB table is created for the parent <small>( the abstract one )</small> model.
- How 
    1. Just like normal model: ```class BaseModel(models.Model)```
    2. The fields are just like before, nothing changed.
    3. The only thing you need to do is 
        - ```class Meta``` :: **```abstract = True```**
    4. For its child <small>( *model* )</small>, it'll be like ```class ChildModel(BaseModel)```
    5. In the side of database, only the ```ChildModel``` table will be created.


### Model inheritance :: *Multi-table model inheritance*
- Features
    1. Each model corresponds <small>( aka 'created' )</small> to a database table.
    2. Quotes from author
        - "Django creates a ```OneToOneField``` field <br>for the relationship in the child's model to its parent"
- How 
    - The only diff is that it doesn't have the ```abstract = True```
    - For its children, just subclassing it: ```class ChildModel(BaseModel)```

### Model inheritance :: *Proxy models*
- Features
    - It was used to ***change the behavoir of a model***.
    - It's kinda like *"split one class into seperated parts"*.
        - Note: either models do have full functionalities.
- How
    1. The *parent* side doesn't need any changes.
    2. Ya need add ```class Meta``` :: **```proxy = True```** to its child.


### A brief summary for these ways of *inheriting*
- All needs to *subclassing* its parent classes.
    - Oh, there's a better version at [here](https://kapeli.com/dash_share?docset_file=Django&docset_name=Django%202.1.3&path=doc/topics/db/models.html%23model-inheritance&platform=django&repo=Versioned%20Main&version=2.1.3) btw.
- Code changes 

    | TYPE | PARENT | CHILDREN | 
    | :-- | :----: | :------: | 
    | Abstract | ```abstract = True``` | \| | 
    | Multi-table | \| | \| | 
    | Proxy | \| | ```proxy = True``` | 