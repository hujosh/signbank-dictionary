# -*- coding: utf-8 -*-
from django.http import Http404
from django.db import models
from tagging.registry import AlreadyRegistered, register
from tagging.models import Tag

class Keyword(models.Model):
    """
    An english keyword that will be a translation of a sign
    """
    def __str__(self):
        return self.text
    text = models.CharField(max_length=100, unique=True)
    
    def inWeb(self):
        """
        Return True if some gloss associated with this
        keyword is in the web version of the dictionary
        """
        return len(self.translation_set.filter(gloss__inWeb__exact=True)) != 0
            
    class Meta:
        ordering = ['text']
        
    class Admin:
        search_fields = ['text']
                
    def match_request(self, request, n):
        """
        Find the translation matching a keyword request given an index 'n'
        response depends on login status
        Returns a tuple (translation, count) where count is the total number
        of matches.
        """
        if request.user.has_perm('dictionary.search_gloss'):
            alltrans = self.translation_set.all()
        else:
            alltrans = self.translation_set.filter(gloss__inWeb__exact=True)     
        # remove crude signs for non-authenticated users if ANON_SAFE_SEARCH is on
        try:
            crudetag = tagging.models.Tag.objects.get(name='lexis:crude')
        except:
            crudetag = None
            
        safe = (not request.user.is_authenticated()) and settings.ANON_SAFE_SEARCH
        if safe and crudetag:
            alltrans = [tr for tr in alltrans if not crudetag in tagging.models.Tag.objects.get_for_object(tr.gloss)]
        
        # if there are no translations, generate a 404
        if len(alltrans) == 0:
            raise Http404
        # take the nth translation if n is in range
        # otherwise take the last
        if n-1 < len(alltrans):
            trans = alltrans[n-1]
        else:
            trans = alltrans[len(alltrans)-1]
        return (trans, len(alltrans))
        
        
class Translation(models.Model):
    """
    An English translations of Auslan glosses
    """
    gloss = models.ForeignKey("Gloss")
    translation = models.ForeignKey("Keyword")
    index = models.IntegerField("Index")
    
    def __str__(self):
        return str(self.gloss)+"-"+str(self.translation)
    
    def get_absolute_url(self):
        """Return a URL for a view of this translation."""
        alltrans = self.translation.translation_set.all()
        idx = 0
        for tr in alltrans: 
            if tr == self:
                return "/dictionary/words/"+str(self.translation)+"-"+str(idx+1)+".html"
            idx += 1
        return "/dictionary/"
        
    class Meta:
        ordering = ['gloss', 'index']
        
    class Admin:
        list_display = ['gloss', 'translation']
        search_fields = ['gloss__idgloss']
    
    
class Gloss(models.Model):
    class Meta:
        verbose_name_plural = "Glosses"
        ordering = ['idgloss']
        permissions = (('update_video', "Can Update Video"),
                       ('search_gloss', 'Can Search/View Full Gloss Details'),
                       ('export_csv', 'Can export sign details as CSV'),
                       ('can_publish', 'Can publish signs and definitions'),
                       ('can_delete_unpublished', 'Can delete unpub signs or defs'),
                       ('can_delete_published', 'Can delete pub signs and defs'),
                       ('view_advanced_properties', 'Include all properties in sign detail view'),
                       ('can_view_unpub_defs', 'Can view unpublished defs'),
                        )

    def __str__(self):
        return "%s-%s" % (self.sn, self.idgloss)
    
    def field_labels(self):
        """
        Return the dictionary of field labels for use in a template
        """
        d = dict()
        for f in self._meta.fields:
            try:
                d[f.name] = self._meta.get_field(f.name).verbose_name
            except:
                pass
        return d

    idgloss = models.CharField("ID Gloss", max_length=50, help_text="""
This is the unique identifying name of an entry of a sign form in the
database. No two Sign Entry Names can be exactly the same, but a "Sign
Entry Name" can be (and often is) the same as the Annotation Idgloss.""")    
  
     # the idgloss used in transcription, may be shared between many signs
    annotation_idgloss = models.CharField("Annotation ID Gloss", blank=True, max_length=30, help_text="""
This is the name of a sign used by annotators when glossing the corpus in
an ELAN annotation file. The Annotation Idgloss may be the same for two or
more entries (each with their own 'Sign Entry Name'). If two sign entries
have the same 'Annotation Idgloss' that means they differ in form in only
minor or insignificant ways that can be ignored.""") 


    sn = models.IntegerField("Sign Number", help_text="Sign Number must be a unique integer and defines the ordering of signs in the dictionary", null=True, blank=True, unique=True)   
            # this is a sign number - was trying
            # to be a primary key, also defines a sequence - need to keep the sequence
            # and allow gaps between numbers for inserting later signs
    inWeb = models.NullBooleanField("In the Web dictionary", default=False)

# register Gloss for tags
try:
    register(Gloss)
except AlreadyRegistered:
    pass

