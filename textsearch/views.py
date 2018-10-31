from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
                        QueryDict
import csv

# Create your views here.

def index(request):
    pass

def search(request):
    if request.method == 'GET':
        url_query_dict = QueryDict(request.META['QUERY_STRING'])

        search_word = url_query_dict.get('word') ## get search argument out 
                                                 ## of querystring 

        ## Open file 
        with open('word_search.tsv', 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            for word in reader:
                print word[0]
        data = {'success': True, 'status': 'printing' }    
    else:
        return HttpResponseBadRequest()
    return JsonResponse(data, safe=True)    
