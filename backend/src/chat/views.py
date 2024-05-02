from django.shortcuts import render
from rest_framework import generics
from src import permissions

from .models import Chat, Message
from .serializers import ChatSerializerNoRef, MessageSerializer


def index(request):
    return render(request, "chat/index.html")


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})


class ChatListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ChatSerializerNoRef
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Chat.objects.filter(user=self.request.user, messages__isnull=False).distinct()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MessageListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        chat_uuid = self.kwargs["chat_uuid"]
        return Message.objects.filter(chat__uuid=chat_uuid, chat__user=self.request.user).select_related("user")

    def perform_create(self, serializer):
        chat_uuid = self.kwargs["chat_uuid"]
        chat = Chat.objects.get(uuid=chat_uuid)
        serializer.save(chat=chat, user=self.request.user)
