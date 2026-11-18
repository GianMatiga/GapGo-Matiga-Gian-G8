from functools import wraps

from django.contrib import messages
from django.contrib.auth.views import redirect_to_login
from django.shortcuts import redirect


def role_required(role):
    """Only allow logged-in users with the given role.
    Logged-out users go to login; other roles go back to their own dashboard."""

    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role != role:
                messages.error(request, "You do not have access to that page.")
                return redirect(request.user.dashboard_url_name)
            return view(request, *args, **kwargs)

        return wrapper

    return decorator
