from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Category, Listing, Comment, Bid


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
        # create new bid
        bid = Bid(
            bid = int(price),
            bidder = owner
        )
        bid.save()
        # create new listing object
        newlisting = Listing(
            title = title,
            description = description,
            price = bid,
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
        comments = Comment.objects.filter(listing=listing_data)
        is_owner = request.user.username == listing_data.owner.username
        return render(request, "auctions/listing.html", {
                "listing": listing_data,
                "in_watchlist": in_watchlist,
                "comments": comments,
                "is_owner": is_owner
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
    bid = request.POST['bid']
    data = Listing.objects.get(pk=id)
    watchlist_data = data.watchlist.all()
    in_watchlist = request.user in watchlist_data
    comments = Comment.objects.filter(listing=data)
    if int(bid) > data.price.bid:
        update = Bid(bidder=request.user, bid=int(bid))
        update.save()
        data.price = update
        data.save()
        return render(request, "auctions/listing.html", {
                "listing": data,
                "in_watchlist": in_watchlist,
                "comments": comments,
                "message": "Your bid was placed. You're the highest bidder now.",
                "update": True
        })
    else:
        return render(request, "auctions/listing.html", {
                "listing": data,
                "in_watchlist": in_watchlist,
                "comments": comments,
                "message": "ERROR! Your bid wasn't placed. Please try again.",
                "update": False
        })

def auctionclosed(request, id):
    data = Listing.objects.get(pk=id)
    data.isActive = False
    data.save()
    watchlist_data = data.watchlist.all()
    in_watchlist = request.user in watchlist_data
    comments = Comment.objects.filter(listing=data)
    return render(request, "auctions/listing.html", {
                "listing": data,
                "in_watchlist": in_watchlist,
                "comments": comments,
                "message": "Auction closed successfully!",
                "update": True
        })

def comment(request, id):
    current_user = request.user
    data = Listing.objects.get(pk=id)
    message = request.POST['newcomment']
    newComment = Comment (
        author = current_user,
        listing = data,
        message = message
    )
    newComment.save()
    return HttpResponseRedirect(reverse("listing", args=(id, )))

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

def closedauctions(request):
    return render(request, "auctions/closedauctions.html", {
        "listings": Listing.objects.filter(isActive=False),
        "categories": Category.objects.all()
    })
