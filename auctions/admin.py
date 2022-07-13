from django.contrib import admin

# Register your models here.
from .models import User, Listing , Category, WatchList, Comment, Bid

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(WatchList)
admin.site.register(Bid)
admin.site.register(Comment)