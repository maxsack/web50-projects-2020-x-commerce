from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True),
        "categories": Category.objects.all()
    })

def categoryfilter(request):
    if request.method == "POST":
        category = request.POST['category']
        cat = Category.objects.get(name=category)
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(isActive=True, category=cat),
            "categories": Category.objects.all()
        })

def createlisting(request):
    if request.method == "GET":
        return render(request, "auctions/createlisting.html", {
            "categories": Category.objects.all()
        })
    else:
        # Get form data
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        img = request.POST["img"]
        cat = request.POST["category"]
        owner = request.user
        # get category data
        category = Category.objects.get(name = cat)
        # create new listing object
        newlisting = Listing(
            title = title,
            description = description,
            price = float(price),
            imageUrl = img,
            owner = owner,
            category = category
        )
        # insert object in database
        newlisting.save()
        #redirect to index page
        return HttpResponseRedirect(reverse("index"))

def listing(request, id):
    if request.method == "GET":
        listing_data = Listing.objects.get(pk=id)
        current_user = request.user
        watchlist_data = listing_data.watchlist.all()
        in_watchlist = current_user in watchlist_data
        return render(request, "auctions/listing.html", {
                "listing": listing_data,
                "in_watchlist": in_watchlist
            })

def watchlist(request):
    current_user = request.user
    listings = current_user.watchlistListing.all()
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def removewatchlist(request, id):
    data = Listing.objects.get(pk=id)
    user = request.user
    data.watchlist.remove(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def addwatchlist(request, id):
    data = Listing.objects.get(pk=id)
    user = request.user
    data.watchlist.add(user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))

def bid(request, id):
    if request.method == "POST":
        bid = request.POST["bid"]
        update_data = Listing.objects.get(pk=id)
        update_data.price = float(bid)
        update_data.save(['price'])
        current_user = request.user
        watchlist_data = update_data.watchlist.all()
        in_watchlist = current_user in watchlist_data
        return render(request, "auctions/listing.html", {
                "listing": update_data,
                "in_watchlist": in_watchlist
            })


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
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })