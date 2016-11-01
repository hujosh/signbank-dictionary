from django.views.generic.detail import DetailView

from dictionary.models import Gloss



class GlossDetailView(DetailView):
    model = Gloss
    context_object_name = 'gloss'
    '''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(GlossDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['tagform'] = TagUpdateForm()
        context['videoform'] = VideoUploadForGlossForm()
        context['definitionform'] = DefinitionForm()
        context['relationform'] = RelationForm()
        context['navigation'] = context['gloss'].navigation(True)
        #context['interpform'] = InterpreterFeedbackForm()
        context['SIGN_NAVIGATION']  = settings.SIGN_NAVIGATION
        if settings.SIGN_NAVIGATION:
            context['glosscount'] = Gloss.objects.count()
            context['glossposn'] =  Gloss.objects.filter(sn__lt=context['gloss'].sn).count()+1
        return context
     '''
  
