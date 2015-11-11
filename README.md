**Build Status:** [![Build Status](https://api.travis-ci.org/jaddison/django-simple-templates.png)](https://travis-ci.org/jaddison/django-simple-templates])


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

So you can see that the A/B testing variation template needs to exist in a directory structure mimicking the original template's directory structure plus its filename without extension.

**Special case:** If you want to create simple page template for the root 'home' page of your website, you given the simple template a special name of ``_homepage_.html``.  URL and directory example:

    <your_templates_dir>/simple_templates/_homepage_.html

would be accessible at:

    http://www.example.com/

If you wanted to create an A/B testing variation template on this page, the simple variation template would exist here:

    <your_templates_dir>/ab_templates/simple_templates/_homepage_/variation2.html

and you'd access it like the examples above:

    http://www.example.com/?ab=variation2


Using A/B Testing in Django Views
----
To use the A/B testing functionality in your existing code, import ``get_ab_template`` and use it in your view:

    from django.shortcuts import render
    from simple_templates.utils import get_ab_template

    def user_signup(request):
        template = get_ab_template(request, 'profiles/user/signup.html')
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

    <your_templates_dir>/profiles/user/signup.html

with a variation called 'fewer-inputs', you would first modify your Django view for a user signing up to use ``get_ab_template`` and you would have this URL as your variation page:

    http://www.example.com/user/signup/?ab=fewer-inputs

and your variation template file should be placed here:

    <your_templates_dir>/ab_templates/profiles/user/signup/fewer-inputs.html


Tips for Optimising your Implementation
----

### SEO Considerations
Speaking plainly, you need to watch that you don't create duplicate content in the eyes of search engines. What's duplicate content? Two pages that are (almost) identical.  When you're doing A/B testing, you're frequently doing minor variations on a theme - perhaps only the colour of a single button.

**Canonical link elements** to the rescue. These are simply an HTML element you place in your ``<head>`` section of your variation template pages, like so:

    <html>
    <head>
        <title>My variation webpage</title>
        <link rel="canonical" href="<< whatever your original page URL is >>">
    </head>
    <body>
        ...
    </body>
    </html>
    
The link represented by ``<< whatever your original page URL is >>`` in the above example should point to the 'canonical' page URL (without the 'ab=variation-name' parameter); meaning the original page URL that you want indexed by search engines.  This way, any search engine that sees a variation template page will 'ignore' it because you're telling it to see it the same as the original page.  But you can make this a lot easier on yourself, by using the excellent [django-spurl](https://github.com/j4mie/django-spurl "django-spurl")  app, and making it this change in your base.html, like so:

    <html>
    <head>
        <title>base.html template</title>
        <link rel="canonical" href="{% block head-canonical %}{% spurl base=request.get_full_path remove_query_param='ab' %}{% endblock %}">
    </head>
    <body>
        ...
    </body>
    </html>

and then extend **all** of your templates (normal view templates, simple templates and A/B templates) from this base.html.  The ``spurl`` template tag simply removes the ``ab`` parameter to create the canonical link for you on **every single page** on your site, making split testing easy, one less thing to think about. Note that you'll need to add the ``django.core.context_processors.request`` to your ``TEMPLATE_CONTEXT_PROCESSORS`` in ``settings.py`` and install [django-spurl](https://github.com/j4mie/django-spurl "django-spurl") for this to work.

### Google Analytics Content Experiments Integration (GACE)
Based on the example above, easy integration for GACE follows a similar strategy - have a ``<head>`` block in your base.html where you can override to place the GACE Javascript snippet, like so:

    <html>
    <head>
        {% block head-gace-js %}{% endblock %}
        <title>base.html template</title>
        <link rel="canonical" href="{% block head-canonical %}{% spurl base=request.get_full_path remove_query_param='ab' %}{% endblock %}">
    </head>
    <body>
        ...
    </body>
    </html>

Then, in any 'original' page that you want to do an A/B test on, you'd override the ``head-gace-js`` block to paste in the GACE JS snippet:

    {% extends 'base.html' %}
    
    {# You would only do this in the original template, not the variation templates! See GACE help for more details. #}
    {% block head-gace-js %}
    ... GACE JS code snippet here
    {% endblock %}

    ... original page's block overrides for content, etc.

I've done a limited amount of testing on the GACE integration, so please report your results!


Running Unit Tests
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
- Django 1.4, 1.5, 1.6, 1.7, 1.9

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
