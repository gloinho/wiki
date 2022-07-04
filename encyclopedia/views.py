from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from . import util
from django import forms
import os
from django.urls import reverse
from random import randint



def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    entry = entry.lower() # uma unica entry
    content = util.get_entry(entry) # lista de entries
    entries = [e.lower() for e in util.list_entries()] # lista de entries lowercase
    if content:
        title = util.list_entries()[entries.index(entry)]
        return render(request, 'encyclopedia/wiki.html', {
            'content': content,
            'title':title,
        })
    else:
        return render(request, './encyclopedia/error404.html')
    
def search_entry(request):
    query_list = request.GET
    query = query_list.get('q').lower()
    entries = [e.lower() for e in util.list_entries()]
    content = util.get_entry(query)
    list_close_entries = []
    if not content:
        for e in entries:
            if query in e:
                list_close_entries.append(util.list_entries()[entries.index(e)])
        if not list_close_entries:
            return entry(request, query) 
        else:
                return render(request, 'encyclopedia/close_search.html', {
                'close_entries': list_close_entries
            })
    else:
        return entry(request, query) 

class NewPage(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control col-sm-10', 'placeholder':'Put a nice title!'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control  col-sm-10', 'placeholder':'Type your content in MarkDown!'}))

def new_page(request):
    if request.method == 'POST':
        form = NewPage(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            try:
                document = title+'.md'
                with open(os.path.join('.\entries', document) , 'x') as new_file:
                    for line in content:
                        new_file.write(line)
                return HttpResponseRedirect(f'wiki/{title}')
            except FileExistsError:
                error = f'The page {title} already exists.'
                return render (request, 'encyclopedia/new_page.html',{
                    'error': error,
                })
    else:
        return render(request, 'encyclopedia/new_page.html', {
            'new_page':NewPage()
        })

class EditPage(forms.Form):
    edit = forms.CharField(widget=forms.Textarea(attrs={'class':'form-control  col-sm-10'}))

def edit_page(request, page):
    data = {'edit':''}
    with open(os.path.join('.\entries',f'{page}.md'), 'r', encoding='utf-8') as editing_page:
        for line in editing_page.readlines():
                data['edit'] += line
        edit = EditPage(data)
    if request.method == 'GET':
        return render(request, 'encyclopedia/edit_page.html', {
            'edit':edit,
            'page':page,
        })
    elif request.method == 'POST':
        form = EditPage(request.POST)
        if form.is_valid():
            content = form.cleaned_data['edit']
            with open(os.path.join('.\entries',f'{page}.md'), 'w', encoding='utf-8') as edited_page:
                edited_page.write(content) # FIXME ta duplicando o \n

            return HttpResponseRedirect(f'/wiki/{page}')
        
        
def random_page(request):
    entries = util.list_entries()
    random_entry = entries[randint(0, len(entries) - 1)]
    return HttpResponseRedirect(f'/wiki/{random_entry}')
    
    


