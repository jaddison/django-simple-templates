from django.shortcuts import render
from django.urls.conf import path

from simple_templates.utils import get_ab_template


def my_view(request):
    return render(request, get_ab_template(request, 'page.html'))


urlpatterns = [
    path('page/', my_view, name='my-page'),
]
