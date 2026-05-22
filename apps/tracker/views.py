from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import F, Q
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
    search = request.GET.get("search", "")
    stocks_query = Stock.objects.filter(
        Q(name__icontains=search)
        | Q(cik__icontains=search)
        | Q(ticker__icontains=search)
        | Q(composite_figi__icontains=search)
        | Q(share_class_figi__icontains=search)
    ).order_by(F(sort).asc(nulls_last=True) if order else F(sort).desc(nulls_last=True))
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


@login_required
def buy_stock_detail(request, stock_id):
    stock = Stock.objects.get(id=stock_id)
    return render(request, f"{tracker_partials}/stock_buy_modal.html", {"stock": stock})
