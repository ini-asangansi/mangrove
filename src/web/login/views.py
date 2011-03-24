# Create your views here.
from uuid import uuid4
import django.contrib.auth as auth
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from services.entity_management.entity_management_service import EntityManagementService
from services.entity_management.models import OrganizationModel
from services.entity_management.organization_id_creator import OrganizationIdCreator
from web.login.forms import RegistrationForm
from services.authentication.authentication_service import AuthenticationService
from services.authentication.models import UserModel
from web.login.forms import LoginForm
from login.decorators import authenticate

SESSION_KEY = 'AUTHETICATED_USER_ID'
BACKEND_SESSION_KEY = 'AUTHETICATED_USER_ID_BACKEND'
SESSION_USER_KEY = 'USER'

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid() :
            user = auth.authenticate(username = form.cleaned_data['email'], password = form.cleaned_data['password'])
            if not user:
                messages.error(request,"Email and password do not match!!!")
                return HttpResponseRedirect(reverse(login))
            else:
                do_login(request, user)
                if request.GET.get('next'):
                    return HttpResponseRedirect(request.GET['next'])
                return render_to_response('home.html',{'username': str(user.name)})
    else:
        form = LoginForm()
    return render_to_response('login.html', {'form' : form}, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() :
            user = UserModel(id=form.cleaned_data.get('email'), email = form.cleaned_data.get('email'), password = form.cleaned_data.get('password')
                             , title = form.cleaned_data.get('title'), first_name = form.cleaned_data.get('first_name'), last_name = form.cleaned_data.get('last_name'))
            org_id=OrganizationIdCreator().generateId()
            organization = OrganizationModel(id=org_id,name = form.cleaned_data.get('organization_name'), sector = form.cleaned_data.get('organization_sector')
                                             , addressline1 = form.cleaned_data.get('organization_addressline1'), addressline2 = form.cleaned_data.get('organization_addressline2')
                                             , city = form.cleaned_data.get('organization_city'), state = form.cleaned_data.get('organization_state')
                                             , country = form.cleaned_data.get('organization_country'), zipcode = form.cleaned_data.get('organization_zipcode')
                                             , office_phone = form.cleaned_data.get('organization_office_phone'), website = form.cleaned_data.get('organization_website')
                                             , administrators = [user.id])
            created_organization = EntityManagementService().create_organization(organization)
            user.organization_id = created_organization.id
            AuthenticationService().create_user(user)
            messages.success(request,"You have successfully registered with id:%s."%(org_id,))
            return HttpResponseRedirect(reverse(login))
    else:
        form = RegistrationForm()
    return render_to_response('register.html', {'form' : form}, context_instance=RequestContext(request))

@authenticate
def logged_in(request):
    user = request.session[SESSION_USER_KEY]
    return render_to_response('home.html',{'username': str(user.name)})

def do_login(request, user):
    if SESSION_KEY in request.session:
        if request.session[SESSION_KEY] != user.id:
            request.session.flush()
    else:
        request.session.cycle_key()
    request.session[SESSION_KEY] = user.id
    request.session[BACKEND_SESSION_KEY] = user.backend
    request.session[SESSION_USER_KEY] = user

