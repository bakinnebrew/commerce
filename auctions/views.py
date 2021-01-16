from .models import User, Listing, Bid, Watchlist, Comment, Winner
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ObjectDoesNotExist
import datetime
from django.contrib.auth.decorators import login_required


class CreateNewListing(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description',
                  'current_price', 'category', 'auction_end_date', 'listing_image']
        exclude = ['owner']


class CreateNewBid(ModelForm):
    class Meta:
        model = Bid
        fields = ['bid_amount']
        exclude = ['user', 'listing_id', 'bit_time']


class CreateNewComment(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        exclude = ['user', 'comment_time', 'listing_id']


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

# function for creating new listing


@login_required(login_url='/login')
def new(request):
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        form = CreateNewListing(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = user
            listing.save()
        return redirect('index')
    else:
        return render(request, "auctions/new.html", {
            "form": CreateNewListing()
        })

# renders html for selected listing


@login_required(login_url='/login')
def listing(request, listing_id):
    user = User.objects.get(username=request.user)
    listing = Listing.objects.get(pk=listing_id)
    comments = Comment.objects.all()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "user": user,
        "comments": comments
    })

# adds listing to watchlist


def add_to_watchlist(request, listing_id):

    if request.method == "POST":
        if request.user.username:
            listing = Listing.objects.get(pk=listing_id)
            user_watchlist = Watchlist.objects.get(user=request.user)
            if listing in user_watchlist.listing_id.all():
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "watchlist_message": "You already have this item in your Watchlist."
                })
            else:
                user = User.objects.get(username=request.user)
                watchlist_items = Watchlist()
                try:
                    user_watchlist.listing_id.add(listing)
                    user_watchlist.save()
                    return HttpResponseRedirect(reverse("watchlist"))

                except Watchlist.DoesNotExist:
                    watchlist_items.user = user
                    watchlist_items.save()
                    watchlist_items.listing_id.add(listing)
                    watchlist_items.save()
                    return HttpResponseRedirect(reverse("watchlist"))

# removes listing from watchlist


def remove_from_watchlist(request, listing_id):
    if request.user.username:
        listing = Listing.objects.get(pk=listing_id)
        user_watchlist = Watchlist.objects.get(user=request.user)
        user_watchlist.listing_id.remove(listing)
        user_watchlist.save()
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": user_watchlist.listing_id.all(),
            "message": "This listing has been removed from your Watchlist"
        })

# watchlist that shows list of listings that have been added to itself


@login_required(login_url='/login')
def watchlist(request):
    if request.method == "GET":
        user_watchlist = Watchlist.objects.get(user=request.user)
        return render(request, "auctions/watchlist.html", {
            "watchlist_items": user_watchlist.listing_id.all()
        })

# shows list of categories user can select


def categories(request):
    listing = Listing()
    categories = listing.get_categories()
    if request.method == "GET":
        return render(request, "auctions/categories.html",  {
            "categories": categories
        })

# shows listings with desired category that was selected with the def categories function


def category_listings(request, category):
    return render(request, "auctions/category_list.html", {
        "listings": Listing.objects.all(),
        "category": category,
    })

# deletes listing


def delete_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        listing.delete()
        return HttpResponseRedirect(reverse("index"))
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Are you sure you want to delete this listing? No bidder will be considered the winner of this auction listing."
        })

# INCOMPLETE
# closes the listing. When closed, the winner of the auction will be notified, unlike deleting listing.


def close_listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        listing.delete()
        return HttpResponseRedirect(reverse("index"))
    if request.method == "GET":
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "close_message": "Are you sure you want to close this listing? The most-recent bidder will become the winner of the auction."
        })

# function for bidding on a listing


@ login_required
def bid(request, listing_id):
    if request.method == "GET":
        listing = Listing.objects.get(pk=listing_id)
        return render(request, "auctions/bid.html", {
            "listing": listing,
            "form": CreateNewBid()
        })
    if request.method == "POST":
        user = User.objects.get(username=request.user)
        listing = Listing.objects.get(pk=listing_id)
        form = CreateNewBid(request.POST)
        if form.is_valid():
            bid = form.save(commit=False)
            bid.user = user
            bid.listing_id = listing
            bid.bid_time = datetime.datetime.now()
            if bid.bid_amount < listing.current_price:
                return render(request, "auctions/bid.html", {
                    "listing": listing,
                    "form": CreateNewBid(),
                    "message": "Bid amount must be more than current price."
                })
            else:
                listing.current_price = bid.bid_amount
                listing.save()
                form.save()
            return HttpResponseRedirect(reverse("listing", args=(listing.id,)))

# function for commenting on a listing


def comment(request, listing_id):
    if request.method == "GET":
        listing = listing = Listing.objects.get(pk=listing_id)
        return render(request, "auctions/comment.html", {
            "listing": listing,
            "comment_form": CreateNewComment()
        })
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        user = User.objects.get(username=request.user)
        comment_form = CreateNewComment(request.POST)
        if comment_form.is_valid():
            comment_form = comment_form.save(commit=False)
            comment_form.user = user
            comment_form.listing_id = listing
            comment_form.comment_time = datetime.datetime.now()
            comment_form.save()
        return HttpResponseRedirect(reverse("listing", args=(listing.id,)))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            Watchlist.objects.create(user=user)
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
