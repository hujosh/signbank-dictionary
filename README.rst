=============================
signbank-dictionary
=============================

.. image:: https://badge.fury.io/py/signbank-dictionary.png
    :target: https://badge.fury.io/py/signbank-dictionary

.. image:: https://travis-ci.org/hujosh/signbank-dictionary.png?branch=master
    :target: https://travis-ci.org/hujosh/signbank-dictionary
    
.. image:: https://codecov.io/gh/hujosh/signbank-dictionary/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/hujosh/signbank-dictionary

The dictionary component of Signbank

Documentation
-------------

The full documentation is at https://signbank-dictionary.readthedocs.org.

Quickstart
----------

Install signbank-dictionary::

    pip install signbank-dictionary

Then use it in a project::

    import dictionary
    
You must define the following variables in ``settings.py``

* ``DEFINITION_FIELDS = ['general', 'noun', 'verb', 'interact', 'diectic', 'modifier', 'question', 'augment', 'note']``
* ``DEFINITION_ROLE_CHOICES = (('general', 'General Definition'),
    ('noun', 'As a Noun'),
    ('verb', 'As a Verb or Adjective'), 
    ('deictic', 'As a Pointing Sign'),
    ('interact', 'Interactive'),
    ('modifier', 'As Modifier'),
    ('question', 'As Question'),
    ('popexplain', 'Popular Explanation'),
    ('augment', 'Augmented Meaning'),
    ('note', 'Note'),
    ('privatenote', 'Private Note'),
    ('B92 sn', 'Sign Number in Brien 92'),
    )``

Those two variables configure how definitions of signs are displayed in
the dictionary.

* ``ALWAYS_TAG_SEARCH = True``
* ``ANON_SAFE_SEARCH = False``

These two variables specify whether an anonymous user (a user who is not
logged in) may search for a sign by tag, and whether signs categorised
as crude (offensive) will be filtered out of the search results for an
anonymous user.

-----------------------------
* ``ALWAYS_REQUIRE_LOGIN`` 
* ``LANGUAGE_NAME``
* ``ANON_TAG_SEARCH``
* ``ANON_SAFE_SEARCH`` 
* ``FORCE_LOWERCASE_TAGS``
* ``ALLOWED_TAGS``
* ``DEFINITION_FIELDS``
* ``SIGN_NAVIGATION``
* ``DEFINITION_ROLE_CHOICES``

``AllOWED_TAGS`` is a list of strings that is used by the ``tagging`` app.
You can copy and paste the following list when you come to defining ``ALLOWED_TAGS`` in
your ``settings.py`` ::
    
    ALLOWED_TAGS = [ '', 
                 'b92:directional',
                 'b92:regional',
                 'corpus:attested',
                 'iconicity:obscure',
                 'iconicity:opaque',
                 'iconicity:translucent',
                 'iconicity:transparent',
                 'lexis:battinson',
                 'lexis:classifier',
                 'lexis:crude',
                 'lexis:doubtlex',
                 'lexis:fingerspell',
                 'lexis:gensign',
                 'lexis:marginal',
                 'lexis:obsolete',
                 'lexis:proper name',
                 'lexis:regional',
                 'lexis:restricted lexeme',
                 'lexis:signed english',
                 'lexis:signed english only',
                 'lexis:technical',
                 'lexis:varlex',
                 'morph:begin directional sign',
                 'morph:body locating',
                 'morph:directional sign',
                 'morph:end directional sign',
                 'morph:locational and directional',
                 'morph:orientating sign',
                 'phonology:alternating',
                 'phonology:dominant hand only',
                 'phonology:double handed',
                 'phonology:forearm rotation',
                 'phonology:handshape change',
                 'phonology:onehand',
                 'phonology:parallel',
                 'phonology:symmetrical',
                 'phonology:two handed',
                 'religion:anglican',
                 'religion:catholic',
                 'religion:catholic school',
                 'religion:jehovas witness',
                 'religion:other',
                 'religion:religion',
                 'semantic:animal',
                 'semantic:arithmetic',
                 'semantic:arts',
                 'semantic:bodypart',
                 'semantic:car',
                 'semantic:city',
                 'semantic:clothing',
                 'semantic:color',
                 'semantic:cooking',
                 'semantic:day',
                 'semantic:deaf',
                 'semantic:drink',
                 'semantic:education',
                 'semantic:family',
                 'semantic:feel',
                 'semantic:food',
                 'semantic:furniture',
                 'semantic:government',
                 'semantic:groom',
                 'semantic:health',
                 'semantic:judge',
                 'semantic:language act',
                 'semantic:law',
                 'semantic:material',
                 'semantic:metalg',
                 'semantic:mind',
                 'semantic:money',
                 'semantic:nature',
                 'semantic:number',
                 'semantic:order',
                 'semantic:people',
                 'semantic:physical act',
                 'semantic:quality',
                 'semantic:quantity',
                 'semantic:question',
                 'semantic:recreation',
                 'semantic:rooms',
                 'semantic:salutation',
                 'semantic:sensing',
                 'semantic:sexuality',
                 'semantic:shapes',
                 'semantic:shopping',
                 'semantic:sport',
                 'semantic:telecommunications',
                 'semantic:time',
                 'semantic:travel',
                 'semantic:utensil',
                 'semantic:weather',
                 'semantic:work',
                 'school:state school',
                 'workflow:needs video',
                 'workflow:redo video',
                 'workflow:problematic',
                 ]
                 
``DEFINITION_FIELDS`` is a list of strings. You can use this in your ``settings.py`` ::

    DEFINITION_FIELDS = ['general', 'noun', 'verb', 'interact', 'diectic', 'modifier', 'question', 'augment', 'note'],
                
``DEFINITION_ROLE_CHOICES`` is a list of tuples. You can use this ::

    DEFINITION_ROLE_CHOICES = (('general', 'General Definition'),
    ('noun', 'As a Noun'),
    ('verb', 'As a Verb or Adjective'), 
    ('deictic', 'As a Pointing Sign'),
    ('interact', 'Interactive'),
    ('modifier', 'As Modifier'),
    ('question', 'As Question'),
    ('popexplain', 'Popular Explanation'),
    ('augment', 'Augmented Meaning'),
    ('note', 'Note'),
    ('privatenote', 'Private Note'),
    ('B92 sn', 'Sign Number in Brien 92')     
              
                
You must also add ``dictionary``, and ``tagging`` to your ``INSTALLED_APPS`` variable.


Features
--------

* TODO

Running Tests
--------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install -r requirements_test.txt
    (myenv) $ python runtests.py

Credits
---------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
