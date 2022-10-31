from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)
    img = models.CharField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.name

class Bid(models.Model):
    bid = models.IntegerField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="biduser")

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=256)
    imageUrl = models.CharField(max_length=1000)
    isActive = models.BooleanField(default=True)
    price = models.ForeignKey(Bid, on_delete=models.CASCADE, blank=True, related_name="pricebid")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True, related_name="category")
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlistListing")

    def __str__(self):
        return self.title
class Comment(models.Model):
    message = models.CharField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name="user_comment")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, related_name="listing_comment")

    def __str__(self):
        return self.message