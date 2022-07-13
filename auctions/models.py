from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    category = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.category}"
    
    
class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing_by_user")
    title= models.CharField(max_length=64)
    desc = models.CharField(max_length=300)
    category = models.ManyToManyField(Category, blank = True, related_name="listing_category")
    starting_bid = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.URLField(default=" ")
    sold = models.BooleanField(default= False)
    
    def __str__(self):
        return f" Item:{self.title}"
    
class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE )
    listing = models.ForeignKey(Listing, on_delete =models.CASCADE, related_name= "userwatchlist")
    watching = models.BooleanField(default = False)

    def __str__(self):
        return f" {self.user} is watching {self.listing}"
    
class Bid(models.Model):
    user= models.ForeignKey(User, on_delete = models.CASCADE, related_name= "bidbyuser")
    listing = models.ForeignKey(Listing, on_delete = models.CASCADE)
    place = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f"{self.user} placed a bid of {self.place} on {self.listing}"
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete =models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment=  models.CharField(max_length=300)
    
    def __str__(self):
        return f" {self.comment} by {self.user}"