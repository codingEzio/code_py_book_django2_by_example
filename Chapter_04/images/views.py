from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse, HttpResponse

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

import redis

from actions.utils import create_action
from common.decorators import ajax_required
from .forms import ImageCreateForm
from .models import Image

# conn to Redis
rds_db = redis.StrictRedis(host=settings.REDIS_HOST,
                           port=settings.REDIS_PORT,
                           db=settings.REDIS_DB)


@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        
        if form.is_valid():
            cleaned = form.cleaned_data
            
            new_item = form.save(commit=False)
            new_item.user = request.user
            
            new_item.save()
            create_action(request.user, 'bookmarked image', new_item)
            
            messages.success(request, 'Image added 😁 !')
            
            return redirect(new_item.get_absolute_url())
    
    else:
        form = ImageCreateForm(data=request.GET)
    
    return render(request,
                  'images/image/create.html', { 'section': 'images',
                                                'form'   : form })


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    
    # the syntax 'xx:xx:xx' ollows the conventions
    #   which is for naming Redis keys (I'll dig more later (maybe))
    total_views = rds_db.incr(f'image:{image.id}:views')
    
    return render(request,
                  'images/image/detail.html', { 'section'    : 'images',
                                                'image'      : image,
                                                'total_views': total_views })


@ajax_required
@login_required
@require_POST
def image_like(request):
    """
        Add a link to the 'image detail' page
            to let users click on it to "like" an image :)
            
        This func is kinda passive (process only)
            it get stuff from the {% block domready %} in <detail.html>
            
        ----- ----- ----- -----
        
        This file is TIGHTLY connected with MULTIPLE files !!
            i.e. the 'ajax' js file & the templates (detail.html)
            
        Lemme explain the code down below
            
            variables
                image_id    id      pk 'id' auto gen_ed by Django (DB-Side)
                action              add who-likes-the-image
                
            JsonResponse
                nothing special, just another if-case
                
        ----- ----- ----- -----
        
        The newly added `@ajax_required`
            is mainly for "users cannot access specific url directly"
            
        Test it by 'YOUR_FULL_URL/images/like/'
            it should be a '400 (Bad request)' (it's inside the devtools)
    """
    
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            
            if action == 'like':
                image.users_like_for_img.add(request.user)
                
                create_action(request.user, 'likes', image)
            
            else:
                image.users_like_for_img.remove(request.user)
            
            return JsonResponse({ 'status': 'ok' })
        
        except Exception:
            pass
    
    return JsonResponse({ 'status': 'ko' })


@login_required
def image_list(request):
    all_images = Image.objects.all()
    
    paginator = Paginator(all_images, 8)
    page = request.GET.get('page')
    
    try:
        all_images = paginator.page(page)
    except PageNotAnInteger:
        all_images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
    
    all_images = paginator.page(paginator.num_pages)
    
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html', { 'section': 'images',
                                                       'images' : all_images })
    
    return render(request,
                  'images/image/list.html', { 'section': 'images',
                                              'images' : all_images })