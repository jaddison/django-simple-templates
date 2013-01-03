django-simple-templates
====

Overview
----
In short, **django-simple-templates** provides easy, designer-friendly templates and A/B testing (split testing) friendly tools for Django.  I ran into both of these problems while working on www.chatterblock.com (which you should check it out).

If you have used or heard of Django's ``flatpages`` app before, you'll be more able to appreciate what **django-simple-templates** gives you.  It is inspired by ``flatpages``, with a desire to have fewer knowledge dependencies and greater flexibility.

Note that this is a work in progress - please provide feedback!

Objectives
----
**django-simple-templates** is intended to:

- provide the means to **isolate template designer effort**; reduce web developer involvement
- provide an easy way to **launch flat or simple pages quickly**; no URL pattern or view needed
- provide a quick and simple method to do **A/B testing (split testing) with Django templates**

Use Cases
----
If you need to quickly launch landing pages for marketing campaigns, then **django-simple-templates** is for you.

If you have a great web designer who knows next to nothing about Django, then **django-simple-templates** is likely a good fit.  It helps to reduce the need for:

- training web designers on Django URL patterns, views, etc. - you can restrict the necessary knowledge to Django templates and template tags (custom and/or builtin)
- involving web developers to create stub page templates or to convert designer-created static HTML pages to Django templates

If you want to be able to **A/B test any Django template** with an external service such as GACE (Google Analytics Content Experiments), then **django-simple-templates** will absolutely help you.  I've always found A/B testing with Django (and frameworks in general) to be somewhat painful - hopefully this app alleviates that pain for others too.

Installation
----
It's a standard PyPi install:

    pip install django-simple-templates

To use the simple page template functionality, add the ``SimplePageFallbackMiddleware`` to your ``MIDDLEWARE_CLASSES`` in your ``settings.py``:

    MIDDLEWARE_CLASSES = (
        ... # other middleware here
        'simple_templates.middleware.SimplePageFallbackMiddleware'
    )

Note that this middleware is not necessary if you only want to use the ``get_ab_template`` functionality (see below).

Configuration Options
----
**django-simple-templates** has a few options to help cater to your project's needs.  You can override these by setting them in your settings.py.  Each has an acceptable default value, so you do not *need* to set them:

- **SIMPLE_TEMPLATES_AB_PARAM**: optional; defaults to ``ab``.  This is the query string (request.GET) parameter that contains the name of the A/B testing template name.
- **SIMPLE_TEMPLATES_AB_DIR**: optional; defaults to ``ab_templates``.  This is the subdirectory inside your TEMPLATE_DIRS where you should place your A/B testing page templates.
- **SIMPLE_TEMPLATES_DIR**: optional; defaults to ``simple_templates``.  This is the subdirectory inside your TEMPLATE_DIRS where you should place your simple page templates.

Usage
----
To create a "simple template" page, all you need to do is create a template file under ``SIMPLE_TEMPLATES_DIR``.  This is your standard Django template format, inheritance, etc.  The directory structure you place it in determines the URL structure.  For example, creating a template here:

    <your_templates_dir>/simple_templates/en/contact.html

would result in the a URL structure like:

    http://www.example.com/en/contact/

The ``SimplePageFallbackMiddleware`` middleware kicks in and looks for possible template file matches when an ``Http404`` is the response to a web request, so if you had a URL pattern and view that handled the ``/en/contact/`` URL, this middleware would not do anything at all.

To create an A/B testing template (the variation template) for the example simple page template above, you'd create the variation template under the appropriate directory structure under ``SIMPLE_TEMPLATES_AB_DIR``:

    <your_templates_dir>/ab_templates/simple_templates/en/contact/variation1.html

and the resulting URL would be:

    http://www.example.com/en/contact/?ab=variation1

To use the A/B testing functionality in your existing code, import ``get_ab_template`` and use it in your view:

    from django.shortcuts import render
    from simple_templates.utils import get_ab_template

    def my_view(request):
        template = get_ab_template(request, 'my_view_template.html')
        return render(request, template)
       
The ``get_ab_template`` function works like this:

- pass Django's `request` object and the view's normal template into `get_ab_template`
- the `get_ab_template` will look in request.GET to see if there was an `ab` parameter in the query string
- if `ab` is found in request.GET, `get_ab_template` will attempt to find the associated template file under ``SIMPLE_TEMPLATES_AB_DIR``
- if the `ab` template file is found, the `ab` template path is returned
- if either `ab` or the template file associated with `ab` is not found, the passed-in 'default' template file is returned

Here's an example to demonstrate.  If you want to A/B test your signup page with the URL:

    http://www.example.com/user/signup/

and your current user signup template file located here:

    <your_templates_dir>/user/signup.html

with a variation called 'fewer-inputs', you would first modify your Django view for a user signing up to use ``get_ab_template`` and you would have this URL as your variation page:

    http://www.example.com/user/signup/?ab=fewer-inputs

and your variation template file should be placed here:

    <your_templates_dir>/ab_templates/user/signup/fewer-inputs.html

Testing
----
To run the **django-simple-templates** tests, follow these steps:

- clone the **django-simple-templates** repository
- change directory into the repository
- initialize a 'virtualenv': ``virtualenv --distribute .``
- activate the virtualenv: ``source bin/activate``
- install the dependencies for testing **django-simple-templates**: ``pip install -r test_project/test-requirements.txt``
- run the tests: ``python test_project/manage.py test simple_templates``

Tests have been run under:
- Python 2.7.3 and Django 1.4.3
- (please report other results)

Compatibility
----
**django-simple-templates** been used in the following version configurations:

- Python 2.6, 2.7
- Django 1.4, 1.5

It should work with prior versions; please report your usage and submit pull requests as necessary.

Source
----
The latest source code can always be found here: http://github.com/jaddison/django-simple-templates/

Credits
----
django-simple-templates is maintained by James Addison, code@scottisheyes.com.

License
----
django-simple-templates is Copyright (c) 2013, James Addison. It is free software, and may be redistributed under the terms specified in the LICENSE file.

Questions, Comments, Concerns:
----
Feel free to open an issue here: http://github.com/jaddison/django-simple-templates/issues/ - or better yet, submit a pull request with fixes and improvements.

TODO:
----
- mention GACE usage (GACE script on original template file only)
- use canonical link tag to non-variation URL (use django-spurl for easy usage)
- build the above into your overall project base.html template(s) so you never forget
- mention `_homepage_` special template case
