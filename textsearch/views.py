from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
                        QueryDict
import csv, re

# Create your views here.

def index(request):
    pass

def search(request):
    if request.method == 'GET':
        url_query_dict = QueryDict(request.META['QUERY_STRING'])
        search_word = url_query_dict.get('word') ## get search argument out 
                                                 ## of querystring 

        ## regular expr that does middle of a word match
        re_midmatch = re.compile('[a-z]+'+search_word+'[a-z]+') 

        ## regular expr for front of a word match
        re_frontmatch = re.compile(search_word+'[a-z]+') 

        match_list = {} ## Change matchlist from set to dict as it is more
                        ## convinient for rankings 
        counter,e, f, m = 0, 0, 0, 0
        ## Open file 
        with open('word_search.tsv', 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            for word in reader:
                if search_word == word[0]:
                    match_list['0'+str(e)] = word[0]
                    counter+=1
                    e+=1
                if re_frontmatch.match(word[0]):
                    match_list['1'+str(f)] = word[0]
                    counter+=1
                    f+=1
                if re_midmatch.match(word[0]):
                    match_list['2'+str(m)] = word[0]
                    counter+=1
                    m+=1

                if counter is 25:
                    break

        realign_keys(match_list)

        data = {'success': True, 'matches': match_list }    
    else:
        return HttpResponseBadRequest()
    return JsonResponse(data, safe=True)    

def realign_keys(dict):
    for key, value in dict.items():
        print key[:1]
