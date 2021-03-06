from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User, Group
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from datawinners.accountmanagement.models import Organization, NGOUserProfile
from datawinners.accountmanagement.forms import OrganizationForm, UserProfileForm

def is_admin(f):

    def wrapper(*args, **kw):
        user = args[0].user
        if not user.groups.filter(name = "NGO Admins").count() > 0:
            return HttpResponseNotFound()

        return f(*args, **kw)
    return wrapper

@login_required(login_url='/login')
@is_admin
def settings(request):
    if request.method == 'GET':
        profile = request.user.get_profile()
        organization = Organization.objects.get(org_id=profile.org_id)
        organization_form = OrganizationForm(instance = organization)
        return render_to_response("account/org_settings.html", {'organization_form' : organization_form}, context_instance=RequestContext(request))

    if request.method == 'POST':
        organization = Organization.objects.get(org_id=request.POST["org_id"])
        organization_form = OrganizationForm(request.POST, instance = organization).update()
        message = "" if organization_form.errors else 'Settings have been updated successfully'
        return render_to_response("account/org_settings.html", {'organization_form' : organization_form, 'message':message}, context_instance=RequestContext(request))
    

@login_required(login_url='/login')
@is_admin
def new_user(request):
    if request.method == 'GET':
        profile_form = UserProfileForm()
        return render_to_response("account/add_user.html", {'profile_form' : profile_form}, context_instance=RequestContext(request))

    if request.method == 'POST':
        org_id = request.user.get_profile().org_id
        form = UserProfileForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not form.errors:
                user = User.objects.create_user(username, username,'test123')
                user.first_name  = form.cleaned_data['first_name']
                user.last_name = form.cleaned_data['last_name']
                group = Group.objects.filter(name = "Project Managers")
                user.groups.add(group[0])
                user.save()
                ngo_user_profile = NGOUserProfile(user = user, title = form.cleaned_data['title'], office_phone = form.cleaned_data['office_phone'],
                                                  mobile_phone = form.cleaned_data['mobile_phone'], skype = form.cleaned_data['skype'], org_id = org_id)
                ngo_user_profile.save()
                reset_form = PasswordResetForm({"email": username})
                reset_form.is_valid()
                reset_form.save(from_email="maheshkl@thoughtworks.com")
                return HttpResponseRedirect('/account/users')


        return render_to_response("account/add_user.html", {'profile_form' : form}, context_instance=RequestContext(request))

@login_required(login_url='/login')
@is_admin
def users(request):
    if request.method == 'GET':
        org_id = request.user.get_profile().org_id
        users = NGOUserProfile.objects.filter(org_id = org_id)
        return render_to_response("account/users_list.html", {'users' : users}, context_instance=RequestContext(request))


@login_required(login_url='/login')
@is_admin
def edit_user(request):
    if request.method == 'GET':
        profile = request.user.get_profile()
        form = UserProfileForm(data = dict(title = profile.title, first_name = profile.user.first_name,
                                           last_name = profile.user.last_name,
                                           username = profile.user.username, office_phone = profile.office_phone,
                                           mobile_phone = profile.mobile_phone,skype = profile.skype))
        return render_to_response("account/edit_profile.html", {'form' : form}, context_instance=RequestContext(request))
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        message = ""
        if form.is_valid():
            user = User.objects.get(username = request.user.username)
            user.first_name  = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.save()
            ngo_user_profile = NGOUserProfile.objects.get(user = user)
            ngo_user_profile.title = form.cleaned_data['title']
            ngo_user_profile.office_phone = form.cleaned_data['office_phone']
            ngo_user_profile.mobile_phone = form.cleaned_data['mobile_phone']
            ngo_user_profile.skype = form.cleaned_data['skype']
            ngo_user_profile.save()
            message = 'Profile has been updated successfully'
        return render_to_response("account/edit_profile.html", {'form' : form, 'message':message}, context_instance=RequestContext(request))

