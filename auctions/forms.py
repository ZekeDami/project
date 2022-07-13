from django.forms import ModelForm
from django import forms


from .models import User, Listing, Category, Bid, Comment, WatchList

class ListingForm(forms.Form):
    title = forms.CharField(label = "Title")
    description = forms.CharField(widget = forms.Textarea(attrs={ 'row':'5', 'col':'50'}))
    bid = forms.CharField(widget= forms.NumberInput(attrs={'step':'0.01', 'min':'0'}))
    category = forms.ModelMultipleChoiceField(queryset=Category.objects.all(), widget=forms.CheckboxSelectMultiple)
    image = forms.CharField(widget=forms.URLInput())
    
    class Meta:
        model = Listing
        fields = ["title", "description","bid", "category", "image"]