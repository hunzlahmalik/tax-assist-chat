from django.urls import path

from . import views

urlpatterns = [
    path("gui/", views.index, name="index"),
    path("gui/<str:room_name>/", views.room, name="room"),
    path(
        "",
        views.ChatListCreateAPIView.as_view(),
        name="chat-list-create",
    ),
    path(
        "<uuid:chat_uuid>/messages/",
        views.MessageListCreateAPIView.as_view(),
        name="message-list-create",
    ),
]
