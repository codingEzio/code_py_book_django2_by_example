# coding=utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST

from common.decorators import ajax_required
from .forms import (
    LoginForm, UserRegistrationForm,
    UserEditForm, ProfileEditForm,
)

from actions.utils import create_action

from actions.models import Action
from .models import Profile, User, Contact


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


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            
            new_user.save()
            
            Profile.objects.create(user=new_user)
            create_action(new_user, 'has created an account')
            
            return render(request,
                          'account/register_done.html', { 'new_user': new_user })
    
    else:
        user_form = UserRegistrationForm()
    
    return render(request,
                  'account/register.html', { 'user_form': user_form })


@login_required
def dashboard(request):
    # not including the actions done by the current user
    actions = Action.objects.exclude(user=request.user)
    
    # the users' id that the current user is following with
    following_ids = request.user.following.values_list('id',
                                                       flat=True)
    
    if following_ids:
        
        # not none (following >=1 user)
        #   get those actions (id <-> action)
        actions = actions.filter(user_id__in=following_ids)
        
        # what about the 'ordering' of the list?
        #   ha! we rely on the one that was specified in the 'Action' model
        #   where? -> the <ordering=('-created')> inside the class 'Meta'
        pass
    
    # ten is enough, lol
    #   old code (slower)
    #   >> actions = actions[:10]
    actions = actions \
                  .select_related('user', 'user__profile') \
                  .prefetch_related('target')[:10]
    
    return render(request,
                  'account/dashboard.html', { 'section': 'dashboard',
                                              'actions': actions })


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Nice! Profile updated 😇')
        
        else:
            messages.error(request, 'Error when updating ur profile 🙁')
    
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request,
                  'account/edit.html', { 'user_form'   : user_form,
                                         'profile_form': profile_form })


@login_required
def user_list(request):
    users = User.objects.filter(is_active=True)
    
    return render(request,
                  'account/user/list.html', { 'section': 'people',
                                              'users'  : users })


@login_required
def user_detail(request, username):
    user = get_object_or_404(User,
                             username=username, is_active=True)
    
    return render(request,
                  'account/user/detail.html', { 'section': 'people',
                                                'user'   : user })


@ajax_required
@require_POST
@login_required
def user_follow(request):
    """
        This one is VERY similar to the <image_like> func in app-image/views.
        
        There are only two options after all (well, true for some cases) :D
    """
    
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user,
                                              user_to=user)
                
                create_action(request.user, 'is following', user)
            
            else:
                Contact.objects.filter(user_from=request.user,
                                       user_to=user).delete()
            
            return JsonResponse({ 'status': 'ok' })
        
        except User.DoesNotExist:
            return JsonResponse({ 'status': 'ko' })
    
    return JsonResponse({ 'status': 'ko' })