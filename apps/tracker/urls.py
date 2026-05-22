from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.home, name="home"),
    path("stocks/", views.all_stocks, name="stocks"),
]

# HTMX endpoints
urlpatterns += [
    path(
        "stocks/buy/<int:stock_id>/detail",
        views.buy_stock_detail,
        name="buy_stock_detail",
    ),
]
