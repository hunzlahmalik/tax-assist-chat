import base64
import json
import uuid

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.core.files.base import ContentFile
from django.db.models import Case, CharField, Value, When
from src.service.groq import GroqService  # Import your GroqService
from src.user.models import User

from .models import Chat, Message  # Import your models
from .serializers import MessageSerializerNoRef


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]

        if self.room_name == "new":
            # create a new room with a random name
            self.room_name = str(uuid.uuid4())

        # check for room name being a valid uuid
        try:
            uuid.UUID(self.room_name)
        except ValueError:
            self.close(
                code=400,
                reason="Invalid room name",
            )
            return

        self.room_group_name = f"chat_{self.room_name}"
        user = self.scope["user"]

        if not user.is_authenticated:
            self.close(
                code=401,
                reason="Unauthenticated",
            )
            return

        self.llm = User.objects.get(username="llm")

        # Create or get the chat room
        chat, created = Chat.objects.get_or_create(name=self.room_name, user=user, uuid=self.room_name)

        # Join room group
        async_to_sync(self.channel_layer.group_add)(self.room_group_name, self.channel_name)

        # Get all messages in the chat room.

        messages = list(
            Message.objects.annotate(
                role=Case(
                    When(user=self.llm, then=Value("assistant")),
                    default=Value("user"),
                    output_field=CharField(),
                ),
            )
            .filter(chat=chat)
            .order_by("-timestamp")
            .values("role", "content")[:100]
        )[::-1]

        self.groq_service = GroqService(messages=messages)

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        user = self.scope["user"]
        file_data = text_data_json.get("file")

        # Save message to the database
        chat = Chat.objects.get(name=self.room_name)
        message_instance = Message.objects.create(
            chat=chat,
            user=user,
            content=message,
        )

        if file_data:
            # If file data exists, handle file upload
            file_content_base64 = file_data.get("data")
            file_content = base64.b64decode(file_content_base64)
            content_file = ContentFile(file_content, name=file_data["name"])

            message_instance.file.save(file_data["name"], content_file, save=True)

        response = self.groq_service.complete_chat_message(message_instance.complete_message)

        message_instance = Message.objects.create(
            chat=chat,
            user=self.llm,
            content=response,
        )

        serialized_message = MessageSerializerNoRef(message_instance)

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                "type": "chat.message",
                "message": serialized_message.data,
            },
        )

    # Receive message from room group
    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps(message))
