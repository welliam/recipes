from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden


def make_ownership_dispatch(get_class):
    """Make ownership based dispatch for use in UpdateViews, DeleteViews, etc.

    `get_class` is a callable which returns the class the dispatch
    method is being overriden upon.

    `related_name` is the name of the objects attached to the
    request's user. If that attribute is not on the user object, the
    user is assumed to be an AnonymousUser (i.e. not logged in).
    """
    def f(self, request, *args, **kwargs):
        if self.request.user.is_anonymous():
            return HttpResponseRedirect(reverse('auth_login'))
        elif self.get_object().user != self.request.user:
            return HttpResponseForbidden()
        else:
            return super(get_class(), self).dispatch(request, *args, **kwargs)
    return f
