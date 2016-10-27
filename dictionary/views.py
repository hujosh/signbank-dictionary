from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tagging.models import Tag, TaggedItem
from django.http import HttpResponse

from dictionary.forms import UserSignSearchForm
from dictionary.models import Gloss, Keyword


def login_required_config(function):
    '''
    Like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True.
    '''
    def wrapper(*args, **kwargs):
        if settings.ALWAYS_REQUIRE_LOGIN:
            decorated_function = login_required(function)
            return decorated_function(*args, **kwargs)
        else:
            return function(*args, **kwargs)
    return wrapper
   
        
@login_required_config
def search(request):
    '''
    Get-variables are either passed to this view or not passed to this view.
    When get-variables are not passed to this view, this view
    displays a form that enables users to search for signs.
    When get-variables are passed to this view, this view
    looks for all signs that correspond to the passed get-variables and
    then returns all corresponding signs to the user.
    '''
    term = ''
    words = []
    form = UserSignSearchForm(request.GET)
    if form.is_valid():
        # need to transcode the query to our encoding
        term = form.cleaned_data['query']
        category = form.cleaned_data['category']
        # safe search for non-authenticated users if the setting says so
        if request.user.has_perm('dictionary.search_gloss'):
            # staff get to see all the words that have at least one translation
            words = Keyword.objects.filter(text__istartswith=term, translation__isnull=False).distinct()
        else:
            # regular users see either everything that's published
            # not sure what is going on here...
            words = Keyword.objects.filter(text__istartswith=term,
                                            translation__gloss__inWeb__exact=True).distinct()        
        safe = (not request.user.is_authenticated()) and settings.ANON_SAFE_SEARCH
        if safe:
            words = remove_crude_words(words)    
        if not category in ['all', '']:
            words = remove_words_not_belonging_to_category(words, category)    
            
    # display the keyword page if there's only one hit and it is an exact match
    if len(words) == 1 and words[0].text == term:
        return redirect('/dictionary/words/'+words[0].text+'-1')
        
    # There might be many hits, so let's paginate them...
    paginator = Paginator(words, 50)
    if 'page' in request.GET:    
        page = request.GET['page']
        try:
            result_page = paginator.page(page)
        except PageNotAnInteger:
            result_page = paginator.page(1)
        except EmptyPage:
            result_page = paginator.page(paginator.num_pages)
    else:
        result_page = paginator.page(1)
    return render(request, "dictionary/search_result.html",
                              {'query' : term,
                               'form': form,
                               'paginator' : paginator,
                               'wordcount' : len(words),
                               'page' : result_page,
                               'ANON_SAFE_SEARCH': settings.ANON_SAFE_SEARCH,                                         
                               'ANON_TAG_SEARCH': settings.ANON_TAG_SEARCH,
                               'language': settings.LANGUAGE_NAME,
                               })

def remove_crude_words(words):
    try:
        crudetag = Tag.objects.get(name='lexis:crude')
    except:
        crudetag = None 
    if crudetag != None:    
        crude = TaggedItem.objects.get_by_model(Gloss, crudetag)
        # remove crude words from result 
        result = []
        for w in words:
            # remove word if all glosses for any translation are tagged crude
            trans = w.translation_set.all()
            glosses = [t.gloss for t in trans]
            if not all([g in crude for g in glosses]):
                result.append(w)
        words = result
    return words
    
def remove_words_not_belonging_to_category(words, category):
    tag = Tag.objects.get(name=category)
    result = []
    for w in words:
        trans = w.translation_set.all()
        glosses = [t.gloss for t in trans]
        for g in glosses:
            if tag in g.tags:
                result.append(w)
    words = result
    return words
    
    
def word(request, keyword, n):
    '''
    View of a single keyword that may have more than one sign.
    '''
    # temporary...
    return HttpResponse("TEST")
