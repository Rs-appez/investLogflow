from functools import wraps
from django.http import HttpResponseForbidden


def htmx_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.headers.get("HX-Request"):
            return HttpResponseForbidden("This endpoint is only accessible via HTMX.")
        return view_func(request, *args, **kwargs)

    return _wrapped_view
