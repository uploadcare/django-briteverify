Django-briteverify
=======================

.. image:: https://img.shields.io/pypi/v/django-briteverify.svg
    :target: https://pypi.python.org/pypi/django-briteverify
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/uploadcare/django-briteverify.svg?branch=master
    :target: https://travis-ci.org/uploadcare/django-briteverify
    :alt: Build status

Helper for easy integration between django and briteverify.com service.

It supports Python2.6+, Django1.4+

Installation
------------

.. code:: bash

    $ pip install django-briteverify

Usage
-----

In common case as you need is use ``BriteverifyFormMixin`` for your forms and specify a ``BRITEVERIFY_API_KEY``:

.. code:: python

    # your_app/forms.py
    from django import forms
    from django_briteverify import BriteverifyFormMixin

    class RegisterForm(BriteverifyFormMixin, forms.Form):
        email = forms.EmailField()


Set ``BRITEVERIFY_API_KEY`` as environment variable:

.. code:: bash

    $ export BRITEVERIFY_API_KEY='YOUR_API_KEY'


Or define it directly in settings

.. code:: python

    # settings.py
    BRITEVERIFY_API_KEY = 'YOUR_API_KEY'

You can specify field name which be used as source for verifying:

.. code:: python

    class RegisterForm(BriteverifyFormMixin, forms.Form):
        another_email = forms.EmailField()

        EMAIL_FIELD_NAME = 'another_email'

Also you can override error messages which raised if validation didn't pass:

.. code:: python

    class RegisterForm(BriteverifyFormMixin, forms.Form):
        error_messages = {
            'invalid_email': _('This is an invalid email address. '
                               'Maybe you mistyped?'),
            'disposable_email': _('Please provide your real email address.')
        }


Contributing
------------

1. Fork the ``django-briteverify`` repo on GitHub.
2. Clone your fork locally:

.. code:: bash

    $ git clone git@github.com:your_name_here/django-briteverify.git

3. Install your local copy into a virtualenv. Assuming you have ``virtualenvwrapper`` installed, this is how you set up your fork for local development:

.. code:: bash

    $ mkvirtualenv django-briteverify
    $ cd django-briteverify/
    $ python setup.py develop

4. Create a branch for local development:

.. code:: bash

    $ git checkout -b name-of-your-bugfix-or-feature

   Now you can make your changes locally.

5. When you're done making changes, check that your changes pass the tests, including testing other Python versions with tox:

.. code:: bash

    $ pip install tox
    $ tox

6. Commit your changes and push your branch to GitHub:

.. code:: bash

    $ git add .
    $ git commit -m "Your detailed description of your changes."
    $ git push origin name-of-your-bugfix-or-feature

7. Submit a pull request through the GitHub website.
