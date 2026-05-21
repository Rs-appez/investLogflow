from django.shortcuts import render
from django.contrib.auth.decorators import login_required

tracker_app = "tracker"


@login_required
def home(request):
    return render(request, f"{tracker_app}/home.html")
