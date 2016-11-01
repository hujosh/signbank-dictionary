from django.conf.urls import include, url

from .dummy_view import dummy


feedback_urls = [  
    # ex: generalfeedback/
    url(r"^generalfeedback/$", dummy,
        name="generalfeedback"),
    # ex: missingsign/
    url(r'^missingsign/$', dummy,
        name='missingsign'),
    # ex: sign/abscond-1/     
    url(r'^word/(?P<keyword>.+)-(?P<n>\d+)/$', dummy,
        name = 'wordfeedback'),
    # ex: gloss/1
    url(r'^gloss/(?P<n>\d+)/$', dummy,
        name = 'glossfeedback')           
]   


urlpatterns = [
    url(r"^", include("dictionary.urls", namespace="dictionary")),
    url(r"^", include(feedback_urls, namespace="feedback")),
]



