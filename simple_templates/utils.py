import os

from django.template import loader, TemplateDoesNotExist
from django.conf import settings


SIMPLE_TEMPLATES_AB_PARAM = getattr(settings, 'SIMPLE_TEMPLATES_AB_PARAM', 'ab')
SIMPLE_TEMPLATES_AB_DIR = getattr(settings, 'SIMPLE_TEMPLATES_AB_DIR', 'ab_templates')


def find_template(template):
    try:
        loader.find_template(template)
        return template
    except TemplateDoesNotExist:
        return None


def get_ab_template(request, default=None):
    """
    This function simply returns the a/b template path if the ab GET parameter exists, otherwise the contents of `default`.

    The path for the ab template is the concatenation of:
     - the SIMPLE_TEMPLATES_AB_DIR setting,
     - the path to the `default` template and
     - the SIMPLE_TEMPLATES_AB_PARAM value from request.GET
    """
    template_name = request.GET.get('ab')
    print template_name
    if template_name:
        if default:
            (filepath, extension) = os.path.splitext(default)
            template_name = os.path.join(SIMPLE_TEMPLATES_AB_DIR, filepath, template_name + extension or '')
            print template_name
        return find_template(template_name) or default
    return default
