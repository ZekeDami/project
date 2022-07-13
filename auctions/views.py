from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Category, Bid, Comment, WatchList
from .forms import ListingForm

def index(request):
    return render(request, "auctions/index.html", {
        "content": Listing.objects.all(),
        
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
    logout (request)
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
    
@login_required
def add(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            user = request.user
            title = form.cleaned_data["title"]
            desc = form.cleaned_data["description"]
            bid = form.cleaned_data["bid"]
            image = form.cleaned_data["image"]
            cat = form.cleaned_data["category"]
            instance=Listing(user=user, title= title, desc = desc, starting_bid= bid, image =image)
            instance.save()
            instance.category.set(cat)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, 'auctions/create_list.html', {
                "listing_form": ListingForm(request.POST),
                "category": Category.objects.all()
            })     
    else:
        return render(request, 'auctions/create_list.html', {
        "listing_form": ListingForm(),
        "category": Category.objects.all()
    })
    
    
@login_required
def about(request, listing_id):
    item = Listing.objects.get(pk=listing_id)
    try:
        items = Bid.objects.get( listing = item, place =item.starting_bid).user
    except(Bid.DoesNotExist):
        create = Bid.objects.create(user = item.user, listing= item, place = item.starting_bid)
        items= create.user
    if request.user == item.user:
        massage = "listed by you"
    else:
        massage = f'listed by {item.user}'
    try:
        watch = WatchList.objects.get(user=request.user,listing=item)
    except(WatchList.DoesNotExist):
        watch = WatchList.objects.create(user= request.user, listing=item)
    if request.user == items and item.sold:
        massage2= "congratulations you have won the auction"
        return render (request, 'auctions/about.html', {
            "item": item,
            "watch": watch.watching,
            "listing_form": ListingForm(),
            "massage": massage,
            "massage2": massage2,
            "comment": Comment.objects.all()
        })
    else:
        return render(request, 'auctions/about.html', {
            "item": item,
            "watch": watch.watching,
            "listing_form":ListingForm(),
            "massage": massage,
            "comment": Comment.objects.all()
        })
    

    
@login_required
def addWatchList(request, listing_id):
    user = request.user
    listing = Listing.objects.get(pk=listing_id)
    watch = WatchList.objects.get(user=user, listing=listing)
    if watch.watching == False:
        watch.watching = True
    else:
        watch.watching =False
    watch.save()
    return HttpResponseRedirect(reverse("about" , args=[listing_id]))


@login_required
def place_bid(request, listing_id):
    item = Listing.objects.get(pk = listing_id)
    if request.method =="POST":
        user= request.user
        nbid = float(request.POST["bid"])
        if nbid > item.starting_bid:
            item.starting_bid = nbid
            Bid.objects.create(user = user, listing=item, place=float(nbid))
            item.save()
        else:
            raise Http404("Bid must be greater than current bid")
    return HttpResponseRedirect(reverse("about", args=[listing_id]))

@login_required
def close_bid(request, listing_id):
    item = Listing.objects.get(pk = listing_id)
    item.sold = True
    item.save()
    return HttpResponseRedirect(reverse("about", args=[listing_id]))

@login_required
def comment(request, listing_id):
    if request.method == "POST":
        user= request.user
        comment = request.POST["comment"]
        listing = Listing.objects.get(pk = listing_id)
        Comment.objects.create(user=user, listing=listing, comment=comment)
        
        return HttpResponseRedirect(reverse("about", args=[listing_id]))
    
@login_required
def Watchlist(request, user_id):
    listing_id = WatchList.objects.filter(user=request.user, watching = True).values('listing')
    listings = Listing.objects.filter(id__in=listing_id)
    return render(request, 'auctions/watch.html', {
        "listings": listings
    })


def category(request):
    listing = None
    cat = Category.objects.all()
    if request.method == "POST":
        cate = Category.objects.get(pk = int(request.POST["categories"]))
        listing= Listing.objects.filter(category= cate)
    return render(request, 'auctions/categories.html',{
        "categories": cat,
        "content":listing
    })