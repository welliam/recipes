from django.urls import reverse
from .models import define_notification_type
from review.models import Review

REVIEW_NOTIFICATION_TEMPLATE = """
"""


@define_notification_type('review', Review)
def format_review_notification(review):
    user_url = reverse(''
    return 
                       .format(review
