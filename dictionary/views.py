from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.shortcuts import render

def login_required_config(f):
    '''
    Like @login_required if the ALWAYS_REQUIRE_LOGIN setting is True.
    '''
    if settings.ALWAYS_REQUIRE_LOGIN:
        return login_required(f)
    else:
        return f
        
        
@login_required_config
def search(request):
    if request.method == 'POST':
        pass
        
    # For any other kind of request...
    else:
        return render(request, 'dictionary/search_result.html')    
