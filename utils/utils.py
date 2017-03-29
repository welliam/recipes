from math import ceil
from django.template.loader import render_to_string
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


def paginate(request, objects, page_param='p', per_page=10):
    """Returns an object with a pages object and relevant objects.

    dict(
      objects=<paginated objects>,
      pages=<rendered pages>
    )"""
    try:
        page = int(request.GET.get(page_param, 1))
    except ValueError:
        page = 1
    uri = request.get_full_path().split('?')[0]
    url_fmtstr = '{}?{}={}'.format(uri, page_param, '{}')
    count = len(objects)
    pages_count = max(ceil(count / per_page), 1)
    return dict(
        pagination_arrows=render_to_string('recipes/pages.html', dict(
            previous_page_url=page != 1 and url_fmtstr.format(page-1),
            next_page_url=page != pages_count and url_fmtstr.format(page+1)
        )),
        objects=objects[(page-1)*per_page:page*per_page]
    )
