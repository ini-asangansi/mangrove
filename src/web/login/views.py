# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from login.forms import RegistrationForm
from services.authentication.authentication_service import AuthenticationService
from services.authentication.models import UserModel
from web.login.forms import LoginForm

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() :
            user = AuthenticationService().authenticate_user(form.cleaned_data['email'].value(), form.cleaned_data['password'].value())
            if not user:
                HttpResponseRedirect(reverse(login))
            else:
                return HttpResponse('You''ve been logged in')
    else:
        form = LoginForm()
    return render_to_response('login.html', {'form' : form}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            user = UserModel(id=form.cleaned_data['email'].value(), email = form.cleaned_data['email'].value(), password = form.cleaned_data['password'].value())
            AuthenticationService().create_user(user)
            HttpResponseRedirect(reverse(login))
    else:
        form = RegistrationForm()
    return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
