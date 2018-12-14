from django import forms
from django.contrib.auth.models import User

from .models import Profile


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


class UserEditForm(forms.ModelForm):
    """
        This one is for users to edit their info (of the built-in Django model)
    """
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileEditForm(forms.ModelForm):
    """
        This one is quite different,
            we allow users to edit the profile data which is created by us :P
    """
    
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')