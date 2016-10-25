from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render

from dictionary.forms import UserSignSearchForm


def login_required_config(function):
    '''
    Like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True.
    '''
    def wrapper(*args, **kwargs):
        if settings.ALWAYS_REQUIRE_LOGIN:
            nonlocal function
            function = login_required(function)
            return function(*args, **kwargs)
        else:
            return function(*args, **kwargs)
    return wrapper
   
        
@login_required_config
def search(request):
    form = UserSignSearchForm(request.GET)
    if form.is_valid():
        # need to transcode the query to our encoding
        term = form.cleaned_data['query']
        category = form.cleaned_data['category']
        # safe search for non-authenticated users if the setting says so
        safe = (not request.user.is_authenticated()) and settings.ANON_SAFE_SEARCH
        
        if request.user.has_perm('dictionary.search_gloss'):
            # staff get to see all the words that have at least one translation
            words = Keyword.objects.filter(text__istartswith=term, translation__isnull=False).distinct()
        else:
            # regular users see either everything that's published
            # not sure what is going on here...
            words = Keyword.objects.filter(text__istartswith=term,
                                            translation__gloss__inWeb__exact=True).distinct()        
        try:
            crudetag = Tag.objects.get(name='lexis:crude')
        except:
            crudetag = None   
        if safe and crudetag != None:    
            crude = TaggedItem.objects.get_by_model(Gloss, crudetag)
            # remove crude words from result 
            
            
               
    return render(request, 'dictionary/search_result.html')    
    
    
