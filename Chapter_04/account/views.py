from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

from .forms import LoginForm


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            input_data = form.cleaned_data
            
            user = authenticate(request,
                                username=input_data['username'],
                                password=input_data['password'])
            
            if user is not None:
                
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully 😆!')
                else:
                    return HttpResponse('Deactivated account 😅')
            
            else:
                return HttpResponse('Invalid login!')
    
    else:
        form = LoginForm()
    
    return render(request,
                  'account/login.html', { 'form': form })