from django.http import HttpResponseBadRequest


def ajax_required(func):
    """
        From my point of view, it's all about
            the specific url (well, it also could opt, no front stuff)
            could not be accessed directly ('ajax-only' in our cases)
    """
    
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest()
        
        return func(request, *args, **kwargs)
    
    wrap.__doc__ = func.__doc__
    wrap.__name__ = func.__name__
    
    return wrap