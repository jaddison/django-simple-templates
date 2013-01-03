from django.conf.urls import patterns, url
from django.shortcuts import render

from simple_templates.utils import get_ab_template


def my_view(request):
    return render(request, get_ab_template(request, 'page.html'))


urlpatterns = patterns('',
    url(r'^page/$', my_view, name='my-page'),
)
