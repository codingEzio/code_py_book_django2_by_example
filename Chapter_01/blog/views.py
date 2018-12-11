from django.core.mail import send_mail
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404

from django.contrib.postgres.search import (
    SearchVector, SearchQuery, SearchRank,
    TrigramSimilarity,
)

from .models import Post, Comment
from .forms import EmailPostForm, CommentForm, SearchForm

from taggit.models import Tag

from django.db.models import Count

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
                  'blog/post/list.html', { 'posts': posts,
                                           'page' : page,
                                           'tag'  : tag })


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
                                        
        Later we added a new feature: 'Tagging'.
            Beyond that, we also could use it for "recommending" related posts.
            
        Just remember that, whenever you're overwhelmed,
            it's just concept, and concepts build on concepts, that's all
            
            For the 'recommending' part, frankly,
                I myself felt a bit frustrated (e.g. I've never seen this var!)
                
            Well, the shitty talk ends here, let's get to the real business.
            
        For the changes for 'recommending' feature (current file only)
            there's just 4 line changes (first 3 for logic, the last is rendering)
            
            Down below is my own understanding #TODO clarify needed
            
            post_tag_ids
                1. cuz we're in the `post_detail`,
                    we ?could easily get infos of the current post
                
                2. so the `post.tags.values_list` is NOT that unreasonable
                    it's just "current-post => its tags => those tag IDs"
                    
                3. okay, now we got the tags ID(s), let's continue :P
                
            X.y.filter().exclude()
                1. get all posts of specific tag ID ("post_tag_ids"'s job)
                2. exclude current post itself (i.e. not recmd the one ur reading)
                
            x.annotate(same_tags=Count('tags'))
                1. we could use `x` & `x.some_tags` #TODO clarify needed
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
    
    # List of similar posts
    post_tag_ids = post.tags.values_list('id', flat=True)
    
    similar_posts = Post.published \
        .filter(tags__in=post_tag_ids) \
        .exclude(id=post.id)
    
    similar_posts = similar_posts \
                        .annotate(same_tags=Count('tags')) \
                        .order_by('-same_tags', '-publish')[:4]
    
    return render(request,
                  'blog/post/detail.html', { 'post'         : post,
                                             'comments'     : comments,
                                             'new_comment'  : new_comment,
                                             'comment_form' : comment_form,
                                             'similar_posts': similar_posts })


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
                  'blog/post/share.html', { 'post': post,
                                            'form': form,
                                            'sent': sent })


def post_search(request):
    """
        The query is actually "not that good" for my own conclusion.
        
        The new (check it by `git log`) one
            is for 'put the more-relevant posts at first' (for search-result)
            
        Two old changes
            
            0)  search_vector
                    SearchVector('title', 'body')
                    SearchVector('title', weight='A') + SearchVector('body', weight='B')
            
            1)  results
                    filter(search=search_query).order_by('-rank')
                    filter(rank__gte=0.3).order_by('-rank')
    """
    
    form = SearchForm()
    query = None
    results = []
    
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        
        if form.is_valid():
            query = form.cleaned_data['query']
            
            search_vector = SearchVector('title', weight='A') \
                            + SearchVector('body', weight='B')
            
            search_query = SearchQuery(query)
            
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('-similarity')
    
    return render(request,
                  'blog/post/search.html', { 'form'   : form,
                                             'query'  : query,
                                             'results': results })