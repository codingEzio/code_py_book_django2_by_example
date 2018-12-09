from django.core.mail import send_mail
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm

from taggit.models import Tag

import os
import sys

sys.path.append(os.path.abspath('../..'))

import sensitive


class PostListView(ListView):
    """
        By using A LOT of 'class-inheritence' & 'mixins',
            a much less code for us to write out the same feature :P
            
        Down below we're just
            (over)writing the attrs & method of (multiple) superclasses.
            
        For the conv between func-based and class-based,
            in our cases, there's not much to changed (it's quite intuitive).
        
        Here's something not THAT INTUITIVE,
            the 'paginator' object used in templates (views-code <-> template)
            
            In func-based ways, the object of 'paginator'
                was assigned to a variable that called 'posts'.
            
            In here, it depends on the (might be multi-levels) superclasses
                it's not that easy
                    to (customize) name a better context name
                    which is specifically for 'paginator' object
            So ...
                what we CAN do is to use the name provided by the superclass
                
            For the 'paginator',
                now you should change the 'posts' (inside `def post_list`)
                to 'page_obj' (where? ./blog/templates/blog/post/list.html)
    """
    model = Post
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'


def post_list(request, tag_slug=None):
    """
        Oh! This is the function-based views!
        
        The `request` here is required (for all views).
    """
    
    # Query
    object_list = Post.published.all()
    
    # Tag
    tag = None
    
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    
    # Paginator
    paginator = Paginator(object_list, 3)  # 3p/page
    
    # current page num
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)  # N pages / 3
    except PageNotAnInteger:
        posts = paginator.page(1)  # invalid (param) => 1st page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # too big => last page
    
    return render(request,
                  'blog/post/list.html', {'posts': posts,
                                          'page' : page,
                                          'tag'  : tag})


def post_detail(request, year, month, day, post):
    """
        Two parts: content &  comment section.
        
        This function very similar to `post_share`.
        
        Content ->  get =>  True    ->  render it
                        =>  False   ->  404
                        
        Comment
            1. existed comments (`post.comments.filter` & `comments`)
            2. words to submit
                ->  GET     ->  display form
                ->  POST    ->  check   ->  True    ->  `save` to DB
                                        ->  False   ->  exec the last line
    """
    
    # Post content
    post = get_object_or_404(Post, slug=post,
                             status='draft',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    # Comment part
    comments = post.comments.filter(active=True)
    new_comment = None
    
    if request.method == 'POST':
        
        comment_form = CommentForm(data=request.POST)
        
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    
    else:
        comment_form = CommentForm()
    
    return render(request,
                  'blog/post/detail.html', {'post'        : post,
                                            'comments'    : comments,
                                            'new_comment' : new_comment,
                                            'comment_form': comment_form})


def post_share(request, post_id):
    """
        GET     ->  display a empty form
        
        POST    ->  submit ur data
                ->  validate by 'is_valid'
                    =>  error   ->  raise it
                    =>  no?     ->  get the data (var 'cd')
                
        Now there's only the last line,
            it is simply rendering what we need.
    """
    
    post = get_object_or_404(Post, id=post_id, status='draft')
    sent = False
    
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        
        if form.is_valid():
            input_email_data = form.cleaned_data
            
            post_url = request.build_absolute_uri(post.get_absolute_url())
            
            subject = '{} ({}) recommends you reading "{}"'.format(
                input_email_data['name'],
                input_email_data['email'],
                post.title
            )
            
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(
                post.title,
                post_url,
                input_email_data['name'],
                input_email_data['comments']
            )
            
            send_mail(
                subject,
                message,
                sensitive.EMAIL_HOST_USER,  # from
                [input_email_data['to']]  # to
            )
            sent = True
    
    else:
        form = EmailPostForm()
    
    return render(request,
                  'blog/post/share.html', {'post': post,
                                           'form': form,
                                           'sent': sent})