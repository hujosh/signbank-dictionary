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

* ``ALWAYS_REQUIRE_LOGIN``
* ``LANGUAGE_NAME``
* ``ANON_TAG_SEARCH``
* ``ANON_SAFE_SEARCH`` 

You must also add ``dictionary`` to your ``INSTALLED_APPS`` variable.


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
