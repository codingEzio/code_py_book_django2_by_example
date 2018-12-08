from django import forms


class EmailPostForm(forms.Form):
    """
        The __Field was conv (or saying "render")
            to related HTML's widget (e.g. CharField => <input>)
            
        And the validation was powered by ?
            Django  the __Field() func itself   e.g. EmailField
            Dev     args being passed in        e.g. max_length=25
    """
    
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False,
                               widget=forms.Textarea)