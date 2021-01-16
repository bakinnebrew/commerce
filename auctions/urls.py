from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("<int:listing_id>", views.listing, name="listing"),
    path("add_to_watchlist/<int:listing_id>",
         views.add_to_watchlist, name="add_to_watchlist"),
    path("remove_from_watchlist/<int:listing_id>",
         views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("new", views.new, name="new"),
    path("<str:category>/listings", views.category_listings, name="category_list"),
    path("categories", views.categories, name="categories"),
    path("bid/<int:listing_id>", views.bid, name="bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("delete_listing/<int:listing_id>",
         views.delete_listing, name="delete"),
    path("close_listing/<int:listing_id>",
         views.close_listing, name="close")
]
