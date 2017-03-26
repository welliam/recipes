from django.shortcuts import render


def notifications_view(request):
    notifications = (
        note
        for note in request.user.notifications.order_by('-date')
        if note.get_object()
    )
    context = dict(notifications=notifications)
    request.user.notifications.update(read=True)
    return render(request, 'notifications.html', context=context)
