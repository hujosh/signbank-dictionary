from django.contrib.auth.decorators import login_required
from django.conf import settings

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
    pass
