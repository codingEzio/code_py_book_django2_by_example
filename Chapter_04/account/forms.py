from django import forms
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    """
        What exactly does the "clean" do?
            In short, <validate & conv-to-consistent-format> :P
            
        Here's the Django's implementation
            Go there by <from django.contrib.auth.forms import UserCreationForm>
    """
    
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password_2nd = forms.CharField(label='Type it again',
                                     widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')
        
    def clean_password_2nd(self):
        """
            The name (i.e. clean_FIELDS) might be a convention,
                that is, for cleaning specific fields (clean & validate) :P
        """
        
        cleaned = self.cleaned_data
        
        if cleaned['password'] != cleaned['password_2nd']:
            raise forms.ValidationError('Password does NOT match!')
        
        return cleaned['password_2nd']