from django.shortcuts import render, get_object_or_404
from .models import Post


def post_list(request):
    """
        Oh! This is the function-based views!
        
        The `request` here is required (for all views).
    """
    
    posts = Post.published.all()
    
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