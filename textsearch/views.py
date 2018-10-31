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
        counter = 0
        ## Open file 
        with open('word_search.tsv', 'r') as infile:
            reader = csv.reader(infile, delimiter='\t')
            for word in reader:
                if search_word == word[0] or re_midmatch.match(word[0]):
                    match_list[counter] = word[0]
                    counter+=1
                if counter is 25:
                    break
        ## replace the square brackets from a list into curly json type brackets
        #curly_match_list = list(match_list).__str__().replace('[', '{') \
        #                                             .replace(']', '}')
        data = {'success': True, 'matches': match_list }    
    else:
        return HttpResponseBadRequest()
    return JsonResponse(data, safe=True)    
