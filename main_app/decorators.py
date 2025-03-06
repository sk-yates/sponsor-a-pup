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