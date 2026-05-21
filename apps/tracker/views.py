from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render

from .models import Stock

tracker_app = "tracker"
tracker_partials = f"{tracker_app}/partials"


@login_required
def home(request):
    return render(request, f"{tracker_app}/home.html")


@login_required
def all_stocks(request):
    pagesize = 20
    page = request.GET.get("page", 1)
    paginator = Paginator(Stock.objects.all(), pagesize)
    stocks = paginator.get_page(page)
    template = (
        f"{tracker_partials}/stocks_table.html"
        if request.headers.get("HX-Request")
        else f"{tracker_app}/stocks.html"
    )
    return render(request, template, {"stocks": stocks})
