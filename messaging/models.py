from django.conf import settings
from django.db import models

from common.models import Audit


class Conversation(Audit):
    TYPE_INDIVIDUAL = "I"
    TYPE_GROUP = "G"

    TYPE_CHOICES = (
        (TYPE_INDIVIDUAL, 'Individual'),
        (TYPE_GROUP, 'Group'),
    )

    type = models.CharField(choices=TYPE_CHOICES, max_length=16)
    name = models.CharField(null=True, blank=True, max_length=255)
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="conversations")
    last_message = models.OneToOneField("Message", null=True, blank=True, related_name="recent_conversation")


class Message(Audit):
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="sent_messages")
    content = models.TextField()
    conversation = models.ForeignKey(Conversation, related_name="messages")
