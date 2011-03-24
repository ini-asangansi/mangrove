from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
import login

REDIRECT_FIELD_NAME = 'next'

def authenticate(target=None):
    """
    Decorator for views that checks that the user is authenticated, redirecting
    to the log-in page if necessary.
    """
    def router(*args):
        user = args[0].session.get('USER')
        if user is not None:
            args[0].user = user
            return target(args[0])
        else:
            return HttpResponseRedirect('/login?%s=%s' % (REDIRECT_FIELD_NAME, args[0].path))
    return router