import markdown2
import random
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util
from .forms import *


def index(request):
    """Default Homepage: displays the list of created entries."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
    })

def entry(request, title):
    entry = util.get_entry(title)
    if entry is None:
        return render(request, "encyclopedia/error.html", {
            "title": title,
            "form": SearchForm()
        })
    else:
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": markdown2.markdown(entry),
            "entry_raw": entry,
            "form": SearchForm()
        })

def search(request):
    if request.method == "POST":
        entries_found = []  
        entries_all = util.list_entries()  
        form = SearchForm(request.POST)  
        if form.is_valid():
            query = form.cleaned_data["query"]
            for entry in entries_all:
                if query.lower() == entry.lower():
                    title = entry
                    entry = util.get_entry(title)
                    return HttpResponseRedirect(reverse("entry", args=[title]))
                if query.lower() in entry.lower():
                    entries_found.append(entry)
            return render(request, "encyclopedia/search.html", {
                "results": entries_found,
                "query": query,
                "form": SearchForm()
            })
    return render(request, "encyclopedia/search.html", {
        "results": "",
        "query": "",
        "form": SearchForm()
    })

def create(request):
    if request.method == "POST":
        new_entry = NewPageForm(request.POST)
        if new_entry.is_valid():
            title = new_entry.cleaned_data["title"]
            data = new_entry.cleaned_data["data"]
            entries_all = util.list_entries()
        
            for entry in entries_all:
                if entry.lower() == title.lower():
                    return render(request, "encyclopedia/create.html", {
                        "form": SearchForm(),
                        "newPageForm": NewPageForm(),
                        "error": "That entry already exists! try to edit it instead. "
                    })
            new_entry_title = "# " + title
            new_entry_data = "\n" + data
            new_entry_content = new_entry_title + new_entry_data
            util.save_entry(title, new_entry_content)
            entry = util.get_entry(title)
            return render(request, "encyclopedia/entry.html", {
                "title": title,
                "entry": markdown2.markdown(entry),
                "form": SearchForm()
            })
    return render(request, "encyclopedia/create.html", {
        "form": SearchForm(),
        "newPageForm": NewPageForm()
    })

def editEntry(request, title):
    """Edit wiki entry"""
    if request.method == "POST":
        entry = util.get_entry(title)
        edit_form = EditPageForm(initial={'title': title, 'data': entry})
        return render(request, "encyclopedia/edit.html", {
            "form": SearchForm(),
            "editPageForm": edit_form,
            "entry": entry,
            "title": title
        })

def submitEditEntry(request, title):
    """submit edit entry wiki"""
    if request.method == "POST":
        edit_entry = EditPageForm(request.POST)
        if edit_entry.is_valid():
            content = edit_entry.cleaned_data["data"]
            title_edit = edit_entry.cleaned_data["title"]
            if title_edit != title:
                filename = f"entries/{title}.md"
                if default_storage.exists(filename):
                    default_storage.delete(filename)
            util.save_entry(title_edit, content)
            entry = util.get_entry(title_edit)
            msg_success = "Successfully updated!"
        return render(request, "encyclopedia/entry.html", {
            "title": title_edit,
            "entry": markdown2.markdown(entry),
            "form": SearchForm(),
            "msg_success": msg_success
        })

def randomEntry(request):
    """random wiki entry"""
    rand_entry_name = random.choice(util.list_entries())
    return redirect('entry', title=rand_entry_name)
