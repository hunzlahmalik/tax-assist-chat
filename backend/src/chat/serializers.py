from rest_framework import serializers
from src.user.serializers import UserSerializer

from .models import Chat, Message


class MessageSerializerNoRef(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ["uuid", "content", "timestamp", "file"]


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = ["uuid", "user", "content", "timestamp", "file"]


class ChatSerializerNoRef(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ["id", "uuid", "name", "description", "timestamp"]


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Chat
        fields = ["id", "uuid", "name", "description", "timestamp", "user", "messages"]
