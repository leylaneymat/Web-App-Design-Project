from django.contrib import admin
from events.models import Event, Ticket, Like, Comment


class TicketInline(admin.StackedInline):
    model = Ticket
    extra = 1


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    inlines = [TicketInline]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
