from django.test import TestCase

from dictionary.models import Keyword, Gloss, Translation

class TestKeyword(TestCase):
    fixtures = ["test_data.json"]
    
    def test_str_method(self):
        keyword = Keyword.objects.get(pk=1)
        self.assertEqual(str(keyword), keyword.text)
        
        
class TestTranslation(TestCase):
    fixtures = ["test_data.json"]
    
    def test_str_method(self):
        translation = Translation.objects.get(pk=1)
        string_of_translation = "%s-%s-%s"%(translation.gloss.sn, 
            translation.gloss.idgloss, translation.translation.text)
        self.assertEqual(str(translation), string_of_translation)
        
        
class TestGloss(TestCase):
    fixtures = ["test_data.json"]
    
    def test_str_method(self):
        gloss = Gloss.objects.get(sn=1)
        self.assertTrue(str(gloss), '%s-%s'%(gloss.sn, gloss.idgloss))
