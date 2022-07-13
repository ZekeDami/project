from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("accounts/login/", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name = "add"),
    path("about/<int:listing_id>", views.about, name = "about"),
    path("watch/<int:listing_id>", views.addWatchList, name="WatchList"),
    path("place/<int:listing_id>", views.place_bid, name= "placebid"),
    path("closebid/<int:listing_id>", views.close_bid, name= "closebid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("watchlist/<int:user_id>", views.Watchlist, name="watch"),
    path("categories", views.category, name="category")
]
