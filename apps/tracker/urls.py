from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.home, name="home"),
    path("stocks/", views.all_stocks, name="stocks"),
    path("portfolios/", views.all_portfolios, name="portfolios"),
]

# POST endpoints
urlpatterns += [
    path("stocks/buy/<int:stock_id>/", views.buy_stock, name="buy_stock"),
    path("portfolios/create/", views.add_portfolio, name="add_portfolio"),
]

# HTMX endpoints
urlpatterns += [
    path(
        "stocks/buy/<int:stock_id>/detail",
        views.buy_stock_detail,
        name="buy_stock_detail",
    ),
]
