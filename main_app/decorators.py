from functools import wraps
from django.shortcuts import redirect

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' not in request.session:
            # Redirect to the custom login view if the user is not authenticated
            return redirect('custom_login')
        return view_func(request, *args, **kwargs)
    return wrapper

def anonymous_required(view_func):
    """
    Decorator for views that ensures only anonymous (not logged-in) users can access the view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Or your designated page for logged-in users.
        return view_func(request, *args, **kwargs)
    return _wrapped_view