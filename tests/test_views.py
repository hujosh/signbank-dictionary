# -*- coding: utf-8 -*-
from django.test import TestCase, RequestFactory
from django.conf import settings 
from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.auth.models import AnonymousUser, User, Permission

from dictionary.views import search



def create_request(url=None, method='GET', data=None, permission=None):
    '''
    This function creates one of various requests. The type
    of request that this function creates depends on the parametres
    of the function.
    
    Call this function in a test case, and use the returned
    request object as an argument to a view. 
    '''
    factory = RequestFactory()
    # Set up the user...
    user = create_user(permission)       
    if 'GET' in method.upper():
        request = factory.get(url)        
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
    def test_search_view_get_request(self):
        '''
        The 'search' view should render 
        'search_result.html' for a get request and
        it should return a response code of 200.
        '''
        request=create_request(method='get')
        with self.assertTemplateUsed('dictionary/search_result.html'):
                response = search(request) 
        self.assertEqual(response.status_code, 200)
                        
  
    
    
