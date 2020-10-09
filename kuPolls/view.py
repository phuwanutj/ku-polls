"""Redirect root urls to index."""
from django.shortcuts import redirect


def index(request):
    """
    Return the index urls.

    :param request is the HttpRequest object.
    """
    return redirect("polls:index")
