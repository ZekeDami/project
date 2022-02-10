from django.shortcuts import render
import markdown2
from django import forms
import random as ran

from . import util

class SearchForm(forms.Form):
    search = forms.CharField(label='', 
    widget=forms.TextInput(attrs={'placeholder':'Search'}))

class NewEntry(forms.Form):
    entry_title = forms.CharField(label='', 
    widget=forms.TextInput(attrs={'placeholder':'Enter Title'}))


class ContentForm(forms.Form):
    content = forms.CharField(label='',
    widget=forms.Textarea(attrs={'placeholder': 'Content', 'row':2, 'col':4}))
    
    
def index(request):
    ser = ""
    search_list = []
    
    if request.method == "POST":
        form = SearchForm(request.POST)

        if form.is_valid():
            ser = form.cleaned_data["search"]

            for title in util.list_entries():
                #if it found correct entry
                if ser.lower() == title.lower():
                    return open(request, title)

                if ser.lower() in title.lower():
                    search_list.append(title)

        if search_list != []:
            return render(request, "encyclopedia/search.html", {
                "poss_search":search_list,
                "form": SearchForm()
            })
        else: 
            return open(request, ser) 

    else:
        return render(request, "encyclopedia/index.html", {
            "entries": util.list_entries(),
            "form": SearchForm()
        })


def open(request, title):
	if util.get_entry(title) is None:
		return render(request, "encyclopedia/error.html" )
	else:
		return render(request, "encyclopedia/title.html", {
            "content": markdown2.markdown(util.get_entry(title)),
            "Page_header": title.capitalize(),
            "form": SearchForm()
        })

def new(request):
    if request.method == "POST":
        form = NewEntry(request.POST)
        form2 = ContentForm(request.POST)
        
        if form.is_valid() and form2.is_valid():
            entry_name = form.cleaned_data["entry_title"]
            entry_content = form2.cleaned_data["content"]
            
            if util.get_entry(entry_name) != None:
                we = "Entry Already Exist"
                return render(request, "encyclopedia/new.html", {
                    "form":SearchForm(),
                    "forms":NewEntry(request.POST),
                    "forms1":ContentForm(request.POST),
                    "entry_exist": we 
                })
            else:
                util.save_entry(entry_name, '#' + entry_name + '/n' + entry_content)
                return open(request, entry_name)
    else:
        return render(request, "encyclopedia/new.html",{
            "forms":NewEntry(),
            "forms1": ContentForm,
            "form": SearchForm()
        })

    
    
def edit(request, title):
    if request.method == "POST":
        form = ContentForm(request.POST)
        if form.is_valid():
            fom = form.cleaned_data["content"]
            util.save_entry(title, fom)
            return open(request, title)
    else:
        markdown_content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html",{
            "Title": title,
            "form": SearchForm(),
            "edit": ContentForm(initial={'content':markdown_content})
        })
    
    
def random(request):
    l  = list(util.list_entries())
    rand_entry = ran.choice(l)
    
    return open(request, rand_entry)
    
    

    
    