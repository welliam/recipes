from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


@login_required
def notifications_view(request):
    notifications = (
        note
        for note in request.user.notifications.order_by('-date')
        if note.get_object()
    )
    context = dict(notifications=notifications)
    request.user.notifications.update(read=True)
    return render(request, 'notifications.html', context=context)


def notification_count_view(request):
    if not request.user.is_authenticated():
        return HttpResponseForbidden()
    count = sum(
        1
        for note in request.user.notifications.order_by('-date')
        if note.get_object() and not note.read
    )
    return JsonResponse(dict(count=count))
