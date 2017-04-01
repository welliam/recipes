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


def format_querystring(d):
    return ';'.join('{}={}'.format(k, d[k]) for k in d)


def format_url(uri, params, page_param, page):
    params[page_param] = page
    return '{}?{}'.format(uri, format_querystring(params))


def paginate(request, objects, page_param='p', per_page=10):
    """Returns an object with a pages object and relevant objects.

    dict(
      objects=<paginated objects>,
      pages=<rendered pages>
    )"""
    params = request.GET.dict()
    try:
        page = max(int(params.get(page_param, 1)), 1)
    except ValueError:
        page = 1
    uri = request.get_full_path().split('?')[0]
    count = len(objects)
    num_pages = max(ceil(count / per_page), 1)
    previous_page = next_page = None
    if page > 1:
        previous_page = format_url(uri, params, page_param, page-1)
    if page <= num_pages:
        next_page = format_url(uri, params, page_param, page+1)
    return dict(
        pagination_arrows=render_to_string('recipes/pages.html', dict(
            previous_page_url=previous_page,
            next_page_url=next_page
        )),
        objects=objects[(page-1)*per_page:page*per_page]
    )
