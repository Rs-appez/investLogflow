from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F
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
    sort = request.GET.get("sort", "ticker")
    order = request.GET.get("order", "asc") == "asc"
    stocks_query = Stock.objects.order_by(
        F(sort).asc(nulls_last=True) if order else F(sort).desc(nulls_last=True)
    )
    paginator = Paginator(stocks_query, pagesize)
    stocks = paginator.get_page(page)
    template = (
        f"{tracker_partials}/stocks_table.html"
        if request.headers.get("HX-Request")
        else f"{tracker_app}/stocks.html"
    )
    response = render(
        request, template, {"stocks": stocks, "sort": sort, "order": order}
    )
    if request.headers.get("HX-Request"):
        params = request.GET.copy()
        for key in params.keys():
            params.setlist(key, [params.get(key)])
        new_url = f"{request.path}?{params.urlencode()}" if params else request.path
        response["HX-Push-Url"] = new_url

    return response
