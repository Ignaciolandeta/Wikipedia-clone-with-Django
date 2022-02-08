from django.forms.forms import Form
import markdown2
import re
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

from django import forms
from . import util


""" class definition for New entry pages via Form """
class newentry(forms.Form):
    title = forms.CharField()
    content = forms.CharField()

class editentry(forms.Form):
    title = forms.CharField()


def index(request):
    """This view function returns a template 'encyclopedia/index.html', providing the template with 
    a list of all of the entries .md in the encyclopedia app (obtained by calling util.list_entries, 
    which is defined in util.py)."""
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def page_entry(request, title):
    """This view get the content of the encyclopedia entry by calling the appropriate util.py function.
    If the entry does exist, the user should be presented with a page that displays the content of the entry. 
    The title of the page should include the name of the entry.
    If an entry is requested that does not exist, 
    the user should be presented with an error page indicating that their requested page was not found.
    """
    page = util.get_entry(title)
    if page:
        markdown2_html = markdown2.markdown(page); """Markdown to HTML Conversion: On each entry’s page, 
        any Markdown content in the entry file should be converted to HTML before being displayed to the user. 
        Use the python-markdown2 package to perform this conversion, installable via pip3 install markdown2.
        For this call 'render' function pass in the 'request' and also pass in the entire HTML page in this case 'entrypage.html' """
        return render(request, "encyclopedia/entrypage.html", {
            "markdown2_html": markdown2_html,
            "title": title
        })
    else:
        return render(request, "encyclopedia/pagenotfound.html")


def searchquery(request):
    """ Search: Allow the user to type a query into the search box in the sidebar to search for an encyclopedia entry."""
    
    if request.method == 'POST':
        """ get the query "q" posted by the user, and if the query matches the name of an encyclopedia entry, 
        the user should be redirected to that entry’s page. 
        https://youtu.be/w8q0C-C1js4?t=5311 """
        q = request.POST['q']
        if util.get_entry(q):
            """ redirect user to search results https://docs.djangoproject.com/en/3.2/ref/urlresolvers/ """
            return HttpResponseRedirect(reverse("encyclopedia:page_entry", kwargs={'title': q }))
        
        else:
            """ If the query does not match the name of an encyclopedia entry, the user should instead be taken to a search results 
        page that displays a list of all encyclopedia entries that have the query as a substring.
        For example, if the search query were 'ytho', then 'Python' should appear in the search results.
        Clicking on any of the entry names on the search results page should take the user to that entry’s page. 
        https://youtu.be/w8q0C-C1js4?t=4988  """
            pages = util.list_entries()
            resultlist = list()
            for page in pages:
                """ import re.search module that scan through string looking for a match 
                (ignore casesensitive with re.IGNORECASE) https://docs.python.org/3/library/re.html """
                if re.search(q, page, re.IGNORECASE):
                    resultlist.append(page)
            return render(request, 'encyclopedia/searchquery.html',{
                "resultlist": resultlist,
                "q": q
            })


def newpage(request):
    """ Clicking “Create New Page” in the sidebar should take the user to a page
     where they can create a new encyclopedia entry.
    Users should be able to enter a title for the page and, 
    in a textarea, should be able to enter the Markdown content for the page.
    Users should be able to click a button to save their new page. """
    if request.method == "POST":
        """ get user input fields'title + content' from Form """
        form = newentry(request.POST)
        if form.is_valid():
            """ When the page is saved, if an encyclopedia entry already exists with the provided title, 
            the user should be presented with an error message.
            Otherwise, the encyclopedia entry should be saved to disk, 
            and the user should be taken to the new entry’s page. 
            https://youtu.be/w8q0C-C1js4?t=5307 """
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not util.get_entry(title):
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('encyclopedia:page_entry', args=(title,)))
            else:
                return render(request, 'encyclopedia/pagenotfound.html')
    return render(request, 'encyclopedia/newpage.html')


def editpage(request):
    """ Edit Page: On each entry page, the user should be able to click a link 
    to be taken to a page where the user can edit that entry’s Markdown content in a textarea. """
    if request.method == "POST":
        form = editentry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            return render(request, 'encyclopedia/editpage.html', {
                "markdown2_html": util.get_entry(title),
                "title": title
            })
            

def editsaved(request):
    if request.method == "POST":
        """When EDIT, get user input fields 'title + content' from Form 
        the same fields when creating 'views.newpage"""
        form = newentry(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:page_entry', args=(title,)))

def rand(request):
        """ Random Page: Clicking “Random Page” in the sidebar 
        should take user to a random encyclopedia entry. """
        
        """ total entries and length; method len() returns the number of elements """
        entries = util.list_entries()
        entrylen = len(entries)
        """ random variable (-1 to be inside range).
        --> Python Random Module - W3Schools
        https://www.w3schools.com/python/module_random.asp
        Python has a built-in module that can be use to make random numbers. """
        randomX = random.randint(0, entrylen) - 1
        """ define 'title' variable and assign random value; """
        title = (entries[randomX])
        return HttpResponseRedirect(reverse('encyclopedia:page_entry', args=(title,)))