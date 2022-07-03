from django.http import HttpResponse
from django.shortcuts import render
from . import util
from django.core.files.storage import default_storage


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
        return render(request, 'encyclopedia/entry.html', {
            'content': content,
            'title':title
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
                list_close_entries.append(e)
        if not list_close_entries:
            return entry(request, query) 
        else:
                return render(request, 'encyclopedia/close_search.html', {
                'close_entries': list_close_entries
            })
    else:
        return entry(request, query) 


""" def close_entry_search(request, query):
    query = query.lower()
    entries = [e.lower() for e in util.list_entries()] # lista de entries lowercase
    content = util.get_entry(query)
    list_close_entries = []
    if not content:
        for entry in entries:
            if query in entry:
                list_close_entries.append(entry)
        if not list_close_entries:
            return False
        else:
                return render(request, 'encyclopedia/close_search.html', {
                'close_entries': list_close_entries
            })
    else:
        return entry(request, query) """

            


        





