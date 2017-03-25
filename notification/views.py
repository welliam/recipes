from django.shortcuts import render


def notifications_view(request):
    notifications = (
        note.render()
        for note in request.user.notifications.all()
        if note.get_object()
    )
    context = dict(notifications=notifications)
    request.user.notifications.update(read=True)
    return render(request, 'notifications.html', context=context)
