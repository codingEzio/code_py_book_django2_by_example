from django import forms
from .models import Comment


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


class CommentForm(forms.ModelForm):
    """
        A little diff from before,
            the forms we'll use was inside the 'models',
            so we need change the 'forms.Form' => 'forms.ModelForm'.
    """
    
    class Meta:
        """
            The variables here indicates
                1. 'model'  ->  where to get the forms
                2. 'fields' ->  what forms should be let fill-in
        """
        
        model = Comment
        fields = ('name', 'email', 'body')


class SearchForm(forms.Form):
    query = forms.CharField()