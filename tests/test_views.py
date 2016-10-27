# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory, override_settings
from django.conf import settings 
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import AnonymousUser, User, Permission
from tagging.models import Tag

from dictionary.views import (search, remove_crude_words, 
    remove_words_not_belonging_to_category)
from dictionary.models import Keyword


def create_request(url=None, method='GET', data=None, permission=None, logged_in=True):
    '''
    This function returns one of various kinds of requests. The kind
    of request that this function returns depends on the parametres
    passed to function.
    
    Call this function in a test case and then use the returned
    request as an argument to a view. 
    '''
    factory = RequestFactory()
    # Set up the user...
    if logged_in:
        user = create_user(permission)
    else:
        user = AnonymousUser()      
    if 'GET' in method.upper():
        request = factory.get(url, data)        
    elif 'POST' in method.upper():
        request = factory.post(url, data)
    else:
        raise ValueError("%s is an unrecognised method. It must be one of 'post' or 'get'"%(method))
    setattr(request, 'session', 'session')
    messages = FallbackStorage(request)
    setattr(request, '_messages', messages)      
    request.user = user      
    return request
    
    
def create_user(permission=None):
    users = User.objects.all()
    nusers = len(users)
    # If a user doesn't exist already...
    if nusers != 1: 
        user = User.objects.create_user(
            username='Jacob', email='jacob@…', password='top_secret', first_name = "Jacob",
            last_name = "smith")
    else:
        # If the user has already been created, use it 
        user = users[0]
    if permission is not None:
        permission = Permission.objects.get(name=permission)
        user.user_permissions.add(permission)             
    return user
   

class SearchView(TestCase):
    fixtures = ["test_data.json"]
    
    def setUp(self):
        self.login_url = '/accounts/login/?next=/None'
             
    def test_search_view_no_get_variables(self):
        '''
        The 'search' view should render 
        'search_result.html' and
        it should return a response code of 200
        when no get variables are passed.
        '''
        request=create_request(method='get')
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request) 
        self.assertEqual(response.status_code, 200)
       
    @override_settings(ALWAYS_REQUIRE_LOGIN=True)
    def test_not_logged_in_and_login_required(self):
        '''
        A user who is not logged in should
        be sent to the login page
        if he requests the search view.
        '''
        request = create_request(logged_in = False)
        response = search(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, self.login_url)                        
    
    @override_settings(ALWAYS_REQUIRE_LOGIN=False)
    def test_not_logged_in_and_login_not_required(self):
        '''
        A user who is not logged in should
        not be sent to the login page
        if he requests the search view.
        '''
        request = create_request(logged_in = False)
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request) 
        self.assertEqual(response.status_code, 200)
        
    def test_remove_crude_words(self):
        '''
        'remove_curde_words' in views.py
        should remove all keywords that are
        tagged 'lexis:crude'.
        '''
        words = Keyword.objects.all()
        # There are nunfiltered keywords in the database
        nunfiltered = len(words)  
        # let's add a crude tag to the first gloss of the first keyword...
        bad_word = words[0]
        bad_gloss = bad_word.translation_set.all()[0].gloss
        Tag.objects.update_tags(bad_gloss, 'lexis:crude')
        # Let's now filter 
        filtered_words = remove_crude_words(words)
        self.assertEqual(nunfiltered-1, len(filtered_words))
        self.assertNotIn(bad_word, filtered_words)

    def test_remove_words_not_belonging_to_category(self):
        '''
        Words not belonging to the category
        'semantic:health' should be removed
        by the function '
        remove_words_not_belonging_to_category'
        '''
        words = Keyword.objects.all()
        # There are nunfiltered keywords in the database
        nunfiltered = len(words)  
        # let's add a health tag to the first gloss of the first keyword...
        health_word = words[0]
        health_gloss = health_word.translation_set.all()[0].gloss
        category = 'semantic:health'
        Tag.objects.update_tags(health_gloss, category)
        # Let's now filter 
        filtered_words = remove_words_not_belonging_to_category(words, category)
        self.assertEqual(1, len(filtered_words))
        self.assertIn(health_word, filtered_words)
         
    def test_search_view_keyword_as_get_variable_no_matches(self):
        '''
        passing a keyeword that matches nothing should 
        render the template 'dictionary/search_result.html'
        ,and should return a response code of 200.
        '''
        request=create_request(method='get', data={'query':'✝'})
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request) 
        self.assertEqual(response.status_code, 200)
             
    def test_search_view_keyword_as_get_variable_1_exact_match(self):
        '''
        passing a keyeword that exactly matches only 1 keyword should 
        redirect to the keyword's gloss page.
        '''
        data={'query':'Aborigine'}
        request=create_request(method='get', data=data)  
        response = search(request) 
        self.assertEqual(response.status_code, 302)
        redirect_url = '/dictionary/words/%s-1'%data['query']
        self.assertTrue(response.url, redirect_url)
    
    def test_search_view_keyword_as_get_variable_inexact_match(self):
        '''
        passing a keyeword that inexactly matches a keyword should 
        render the template 'dictionary/search_result.html'
        ,and should return a response code of 200.
        '''
        request=create_request(method='get', data={'query':'Aborigin'})
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request) 
        self.assertEqual(response.status_code, 200)
    
    

