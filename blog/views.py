from django.shortcuts import render
from django.http.response import HttpResponse
from django.views import generic

from Django_Blog import utils


@utils.decorator_cache(time_out=60 * 60)
def get_cache():
    return 3


def index(request):
    x = get_cache()

    return HttpResponse(str(x))
