'''
The dictionary app, in various places, tries to resolve urls defined in 
the feedback app. Since the dictionary app is independent from the 
feedback app, it cannot go to the feedback app to resolve these urls. Intead,
I re-define the feedback urls referened by the dictionary app in 
test/test_urls.py. These urls require a view, and this file provides that view.
'''
from django.http import HttpResponse


def dummy(request):
    return HttpResponse("Django's independent app idea doesn't work.")
    
    
