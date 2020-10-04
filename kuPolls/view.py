"""Redirect root urls to index."""
from django.shortcuts import redirect


def index(request):
    """Return the index urls."""
    return redirect("polls:index")
