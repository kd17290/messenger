from rest_framework import serializers

from common.serializers import UserSerializer
from messaging.models import Message, Conversation


class MessageSerializer(serializers.ModelSerializer):

    from_user = UserSerializer()

    class Meta:
        model = Message
        fields = ('id', 'content', 'from_user', 'created')


class RecentConversationSerializer(serializers.ModelSerializer):

    message = MessageSerializer(source="last_message")

    class Meta:
        model = Conversation
        fields = ("id", "message")


class UserRecentMessageSerializer(UserSerializer):

    recent_conversations = RecentConversationSerializer(many=True)

    class Meta(UserSerializer.Meta):
        fields = ('id', 'username', 'recent_conversations')


class CreateIndividualMessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = ("id", "content", "from_user")
