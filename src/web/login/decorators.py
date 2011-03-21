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
        if args[0].session.get('USER') is not None:
            return target(args)
        else:
            return HttpResponseRedirect('/login?%s=%s' % (REDIRECT_FIELD_NAME, args[0].path));
    return router