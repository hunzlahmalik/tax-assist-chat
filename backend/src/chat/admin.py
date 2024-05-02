from django.contrib import admin

from .models import Chat, Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ("uuid", "name", "description", "timestamp")
    search_fields = ("uuid", "name", "description")
    readonly_fields = ("uuid", "timestamp")


class MessageAdmin(admin.ModelAdmin):
    list_display = ("uuid", "chat", "user", "content", "timestamp")
    search_fields = ("uuid", "chat", "user", "content")
    readonly_fields = ("uuid", "timestamp")


admin.site.register(Chat, ChatAdmin)

admin.site.register(Message, MessageAdmin)
