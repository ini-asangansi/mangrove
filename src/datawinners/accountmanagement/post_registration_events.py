# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from datawinners.accountmanagement.models import NGOUserProfile


def ngo_user_created(sender, user, request, **kwargs):
    data = NGOUserProfile()
    data.org_id = kwargs['organization_id']
    data.title = kwargs['title']
    data.user = user
    data.save()
