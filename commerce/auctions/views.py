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
        cat = Category.objects.get(categoryName=category)
        return render(request, "auctions/index.html", {
            "listings": Listing.objects.filter(isActive=True, category=cat),
            "categories": Category.objects.all()
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

def watchlist(request):
    return render(request, "auctions/watchlist.html")

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
        category = Category.objects.get(categoryName = cat)
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

def listing(request):
    return render(request, "auctions/listing.html")