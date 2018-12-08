from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404
from .models import Post


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


def post_list(request):
    """
        Oh! This is the function-based views!
        
        The `request` here is required (for all views).
    """
    
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)  # 3p/page
    
    # current page num
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)  # N pages / 3
    except PageNotAnInteger:
        posts = paginator.page(1)  # invalid (param) => 1st page
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)  # too big => last page
    
    return render(
        request,  # required
        'blog/post/list.html',  # template path
        {'posts': posts}  # context name (aha!)
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='draft',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    
    return render(
        request,
        'blog/post/detail.html',
        {'post': post},
    )