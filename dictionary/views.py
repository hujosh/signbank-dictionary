from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tagging.models import Tag, TaggedItem
from django.http import HttpResponse, Http404

from dictionary.forms import UserSignSearchForm, TagUpdateForm
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
            words = Keyword.objects.filter(text__istartswith=term, 
                translation__isnull=False).distinct()
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
    # Display the keywords, 50 per page...
    (result_page, paginator) = paginate(request, words, 50)
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
    
    
def paginate(request, objects, npages):
    # There might be many matches, so let's paginate them...
    paginator = Paginator(objects, npages)
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
    return (result_page, paginator)
    
    
def word(request, keyword, n):
    '''
    View of a single keyword that may have more than one sign.
    '''
    n = int(n)
    word = get_object_or_404(Keyword, text=keyword)
    # returns (matching translation, number of matches)
    (trans, total) =  word.match_request(request, n)
    # and all the keywords associated with this sign
    allkwds = trans.gloss.translation_set.all()
    '''
    videourl = trans.gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None
    '''
    trans.homophones = trans.gloss.relation_sources.filter(role='homophone')

    can_view_not_inWeb = request.user.has_perm('dictionary.search_gloss')
    gloss = trans.gloss
    (glossposn, glosscount) = get_gloss_position(gloss, can_view_not_inWeb)
    
    # navigation gives us the next and previous signs
    nav = gloss.navigation(request.user.has_perm('dictionary.search_gloss'))
    
    '''
    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=trans.gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_id': trans.gloss.pk,
                                                      'redirect': request.path})
    else:
        update_form = None
        video_form = None
    '''
    '''
    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None
    
    '''
    
    
    return render(request, 'dictionary/word.html',
                    {'translation': trans,
                   'viewname': 'words',
                   'definitions': trans.gloss.definitions(),
                   'gloss': trans.gloss,
                   'allkwds': allkwds,
                   'n': n,
                   'total': total,
                   'matches': range(1, total+1),
                   'navigation': nav,
                   #'dialect_image': map_image_for_regions(gloss.region_set),
                   #'regions': regions,
                   #'regional_template_content': regional_template_content,
                   # lastmatch is a construction of the url for this word
                   # view that we use to pass to gloss pages
                   # could do with being a fn call to generate this name here and elsewhere
                   'lastmatch': str(trans.translation)+"-"+str(n),
                   #'videofile': videourl,
                   #'update_form': update_form,
                   #'videoform': video_form,
                   'gloss': gloss,
                   'glosscount': glosscount,
                   'glossposn': glossposn,
                   #'feedback' : True,
                   #'feedbackmessage': feedbackmessage,
                   'tagform': TagUpdateForm(),
                   'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                   'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                   })

@login_required_config
def gloss(request, idgloss):
    '''
    View of a gloss - mimics the word view, really for admin use
    when we want to preview a particular gloss
    '''
    '''
    if request.GET.has_key('feedbackmessage'):
        feedbackmessage = request.GET['feedbackmessage']
    else:
        feedbackmessage = False
    '''
    # we should only be able to get a single gloss, but since the URL
    # pattern could be spoofed, we might get zero or many
    # so we filter first and raise a 404 if we don't get one
    can_view_not_inWeb = request.user.has_perm('dictionary.search_gloss')
    if can_view_not_inWeb:
        glosses = Gloss.objects.filter(idgloss=idgloss)
    else:
        glosses = Gloss.objects.filter(inWeb__exact=True, idgloss=idgloss)

    if len(glosses) != 1:
        raise Http404

    gloss = glosses[0]

    # and all the keywords associated with this sign
    allkwds = gloss.translation_set.all()
    if len(allkwds) == 0:
        trans = Translation()
    else:
        trans = allkwds[0]
    '''
    videourl = gloss.get_video_url()
    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, videourl)):
        videourl = None
    '''
    (glossposn, glosscount) = get_gloss_position(gloss, can_view_not_inWeb)
    
    # navigation gives us the next and previous signs
    nav = gloss.navigation(can_view_not_inWeb)

    # the gloss update form for staff
    update_form = None
    '''
    if request.user.has_perm('dictionary.search_gloss'):
        update_form = GlossModelForm(instance=gloss)
        video_form = VideoUploadForGlossForm(initial={'gloss_id': gloss.pk,
                                                      'redirect': request.get_full_path()})
    else:
        update_form = None
        video_form = None
        
    '''
    # get the last match keyword if there is one passed along as a form variable
    if 'lastmatch' in request.GET:
        lastmatch = request.GET['lastmatch']
        if lastmatch == "None":
            lastmatch = False
    else:
        lastmatch = False
    '''
    # Regional list (sorted by dialect name) and regional template contents if this gloss has one
    regions = sorted(gloss.region_set.all(), key=lambda n: n.dialect.name)
    try:
        page = Page.objects.get(url__exact=gloss.regional_template)
        regional_template_content = mark_safe(page.content)
    except:
        regional_template_content = None
    '''

    return render(request, "dictionary/word.html",
                              {'translation': trans,
                               'definitions': gloss.definitions(),
                               'allkwds': allkwds,
                               #'dialect_image': map_image_for_regions(gloss.region_set),
                               #'regions': regions,
                               #'regional_template_content': regional_template_content,
                               'lastmatch': lastmatch,
                               #'videofile': videourl,
                               'viewname': word,
                               #'feedback': None,
                               'gloss': gloss,
                               'glosscount': glosscount,
                               'glossposn': glossposn,
                               'navigation': nav,
                               #'update_form': update_form,
                               #'videoform': video_form,
                               'tagform': TagUpdateForm(),
                               #'feedbackmessage': feedbackmessage,
                               'SIGN_NAVIGATION' : settings.SIGN_NAVIGATION,
                               'DEFINITION_FIELDS' : settings.DEFINITION_FIELDS,
                               })


def get_gloss_position(gloss, can_view_not_inWeb):
    '''
    This functions returns a tuple; the first value
    of the tuple is the gloss's position relative
    to all of the other glosses, and the second value
    is the total number of glosses.
    
    If gloss_must_be_in_web is true, then only glosses
    that are in the web will be considered.
    '''
    if gloss.sn != None:
        if  can_view_not_inWeb:
            glosscount = Gloss.objects.count()
            glossposn = Gloss.objects.filter(sn__lt=gloss.sn).count()+1
        else:
            glosscount = Gloss.objects.filter(inWeb__exact=True).count()
            glossposn = Gloss.objects.filter(inWeb__exact=True, 
                sn__lt=gloss.sn).count()+1
    else:
        glosscount = 0
        glossposn = 0
    return (glossposn, glosscount)
    

    
    
    
    
    
