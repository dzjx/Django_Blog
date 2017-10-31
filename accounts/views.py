from django.shortcuts import render
from django.views import generic


# Create your views here.

class LoginView(generic.RedirectView):
    pass


class LogoutView(generic.RedirectView):
    pass