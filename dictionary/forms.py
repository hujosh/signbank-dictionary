from django import forms
from django.conf import settings

class UserSignSearchForm(forms.Form):
    # category choices are tag values that we'll restrict search to
    CATEGORY_CHOICES = (('all', 'All Signs'),
        ('semantic:health', 'Only Health Related Signs'),
        ('semantic:education', 'Only Education Related Signs'))
    query = forms.CharField(label='Keywords starting with', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    category = forms.ChoiceField(label='Search', choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control'}))
    

class TagUpdateForm(forms.Form):
    """Form to add a new tag to a gloss"""
    tag = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control'}), 
                            choices=[(t, t) for t in settings.ALLOWED_TAGS])
    delete = forms.BooleanField(required=False, widget=forms.HiddenInput)
