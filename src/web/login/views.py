# Create your views here.
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from login.forms import RegistrationForm

def login(request):
    return render_to_response('login.html')

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            HttpResponseRedirect(reverse(login))
    else:
        form = RegistrationForm()
    return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))
