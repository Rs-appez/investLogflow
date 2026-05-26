from django.urls import path
from . import views

app_name = "tracker"

urlpatterns = [
    path("", views.home, name="home"),
    path("stocks/", views.all_stocks, name="stocks"),
]

# POST endpoints
urlpatterns += [
    path("stocks/buy/<int:stock_id>/", views.buy_stock, name="buy_stock"),
]

# HTMX endpoints
urlpatterns += [
    path(
        "stocks/buy/<int:stock_id>/detail",
        views.buy_stock_detail,
        name="buy_stock_detail",
    ),
]
