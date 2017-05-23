# Create your views here.
from django.contrib.auth import get_user_model
from django.db.models.aggregates import Max, Sum
from django.db.models.expressions import Case, When, F
from django.db.models.fields import IntegerField
from django.db.models.query import Prefetch
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination

from messaging.models import Message, Conversation
from messaging.serializers import UserRecentMessageSerializer, CreateIndividualMessageSerializer, MessageSerializer


class RecentConversationsView(ListAPIView):
    # .annotate(last_message_id=Max('conversations__last_message')) \
    # .filter(last_message_id__isnull=False)\
    queryset = get_user_model().objects.all()\
        .annotate(last_message_id=Max("conversations__last_message"))\
        .prefetch_related(Prefetch('conversations', queryset=Conversation.objects.filter(last_message_id=F("last_message_id")), to_attr="recent_conversations"))
    serializer_class = UserRecentMessageSerializer
    pagination_class = LimitOffsetPagination


class SendMessageView(CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = CreateIndividualMessageSerializer

    def perform_create(self, serializer):
        from_user = serializer.validated_data["from_user"]
        to_user_id = self.request.data.get("to_user")
        to_user = get_user_model().objects.filter(pk=to_user_id).first()
        if not to_user:
            raise ValidationError({"message": "Invalid recipient"})
        if to_user == from_user:
            raise ValidationError({"message": "Please provide different sender and recipient"})
        existing_conversation = Conversation.objects.filter(type=Conversation.TYPE_INDIVIDUAL)\
            .annotate(from_user_exists=Sum(Case(When(users=from_user, then=1), output_field=IntegerField())))\
            .annotate(to_user_exists=Sum(Case(When(users=to_user, then=1), output_field=IntegerField())))\
            .filter(from_user_exists__gt=0, to_user_exists__gt=0).first()
        if not existing_conversation:
            existing_conversation = Conversation.objects.create(type=Conversation.TYPE_INDIVIDUAL)
            existing_conversation.users.add(from_user)
            existing_conversation.users.add(to_user)
        serializer.save(conversation=existing_conversation)
        existing_conversation.last_message = serializer.instance
        existing_conversation.save()


class UserMessagesView(ListAPIView):

    serializer_class = MessageSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        existing_conversation = Conversation.objects.filter(type=Conversation.TYPE_INDIVIDUAL) \
            .annotate(from_user_exists=Sum(Case(When(users__id=self.kwargs.get("from"), then=1), output_field=IntegerField()))) \
            .annotate(to_user_exists=Sum(Case(When(users__id=self.kwargs.get("to"), then=1), output_field=IntegerField()))) \
            .filter(from_user_exists__gt=0, to_user_exists__gt=0).first()
        if not existing_conversation:
            return Message.objects.none()
        return existing_conversation.messages.order_by('-created')
