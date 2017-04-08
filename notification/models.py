from django.template.loader import get_template
from django.db import models
from django.contrib.auth.models import User
from review.models import Review
from recipe.models import Recipe


NOTIFICATION_TYPES = {}


class NotificationType(object):
    def __init__(self, model, template_name):
        self.template_name = template_name
        self.model = model
        self.template = get_template(self.template_name)

    def find(self, pk):
        return self.model.objects.filter(pk=pk).first()

    def render(self, obj):
        return self.template.render(context={'object': obj})


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.deletion.CASCADE
    )
    type = models.CharField(max_length=20)
    object_key = models.IntegerField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def get_object(self):
        model = NOTIFICATION_TYPES[self.type].model
        return model.objects.filter(id=self.object_key).first()

    def render(self):
        search = self.get_object()
        if search is None:
            raise ValueError('Object not found')
        return NOTIFICATION_TYPES[self.type].render(search)


def define_notification_type(type, model, template_name):
    NOTIFICATION_TYPES[type] = NotificationType(model, template_name)


define_notification_type('review', Review, 'notifications/review.html')

define_notification_type('follow', User, 'notifications/follow.html')

define_notification_type('derive', Recipe, 'notifications/derive.html')
