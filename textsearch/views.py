from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest, \
                        QueryDict
from django.shortcuts import render
import csv, re 

# Create your views here.

def index(request):
    return render(request, 'index.html')

def search(request):
    """ Search query handler """

    if request.method == 'GET':
        url_query_dict = QueryDict(request.META['QUERY_STRING'])
        search_word = url_query_dict.get('word') ## get search argument out 
                                                 ## of querystring 

        ## exit if no search query
        if not search_word:
            return JsonResponse({'success': False, 'status': 'no query'}, \
                                  safe=True)    

        ## regular expr that does middle of a word match
        re_midmatch = re.compile('[a-z]+'+search_word+'[a-z]+') 

        ## regular expr for front of a word match
        re_frontmatch = re.compile(search_word+'[a-z]+') 

        match_list = {} ## Change matchlist from set to dict as it is more
                        ## convinient for rankings 
        counter = e = f = m = 0 ## all counters to zero

        with open('word_search.tsv', 'r') as infile: ## open file
            reader = csv.reader(infile, delimiter='\t')
            for word in reader: ## loop through reader obj line by line

                ## In case of an exact match
                if search_word == word[0]: 
                    match_list['0'+str(e)] = word[0] ## the top part of 
                    ## match_list dict, the trailing zero is rank scheme 
                    counter+=1
                    e+=1

                ## In case of a 'prefix' match
                if re_frontmatch.match(word[0]):
                    match_list['1'+str(f)] = word[0] ## the middle part of list
                    ## composed of words that start with search query
                    counter+=1
                    f+=1

                ## mmiddle match
                if re_midmatch.match(word[0]):
                    match_list['2'+str(m)] = word[0] ## when query string lies
                    ## in the middle of the word these words form the lower portion                    ## of match_list
                    counter+=1
                    m+=1

                if counter is 25: ## counter to keep track of match_list items
                    break

        sorted_match_list = realign_dict_to_list(match_list)

        data = {'success': True, 'matches': sorted_match_list }    
    else:
        return HttpResponseBadRequest() ## bad request if request is not GET
    return JsonResponse(data, safe=True)    

def realign_dict_to_list(dict):
    """ convert unsorted dict to sorted list using the keys"""
    sorted_list = []
    od_fp = sorted(dict.keys(), cmp=p_cmp)
    for index in od_fp:
        sorted_list.append(dict[index])
    return sorted_list

def p_cmp(a, b):
    """ 
    Custom comparator function that expects first integer of key and remaining 
    integers in key as separate order encoding and returns proper comparison 
    relation between them

    """    
    if int(a[:1]) == int(b[:1]):
        if int(a[1:]) < int(b[1:]):
            return -1
        elif int(a[1:]) > int(b[1:]):
            return 1
    elif int(a[:1]) < int(b[:1]): 
        return -1   
    else:
        return 1
