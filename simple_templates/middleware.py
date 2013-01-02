from django.conf import settings
from django.shortcuts import render, redirect

from .utils import get_ab_template, find_template


SIMPLE_TEMPLATES_DIR = getattr(settings, 'SIMPLE_TEMPLATES_DIR', 'simple_templates')


class SimplePageFallbackMiddleware(object):
    def process_response(self, request, response):
        # No need to check for a simple template for non-404 responses.
        if response.status_code != 404:
            return response

        # set up the location where this template should reside
        template = "{0}/{1}.html".format(SIMPLE_TEMPLATES_DIR, request.path.strip('/') or '_homepage_')
        print template

        # if it doesn't exist, continue with the 404 response
        if not find_template(template):
            return response

        # if the template exists, ensure the trailing slash is present and redirect if necessary
        if not request.path.endswith('/') and settings.APPEND_SLASH:
            url = request.path + "/"
            qs = request.META.get('QUERY_STRING')
            if qs:
                url += '?' + qs
            return redirect(url, permanent=True)

        # check for the presence of an a/b test template page
        return render(request, get_ab_template(request, template))
