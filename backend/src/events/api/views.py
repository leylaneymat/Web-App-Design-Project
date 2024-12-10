from django.shortcuts import get_object_or_404
from django.db.utils import IntegrityError
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound

from events.models import Event, Ticket, Like, Comment
from events.api.serializers import EventSerializer, TicketSerializer, LikeSerializer, CommentSerializer
from events.permissions import IsAdminOrReadOnly, IsAdminOrIsOwnerOrReadOnly
from events.models import User



class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    lookup_url_kwarg = "event_pk"
    permission_classes = [IsAdminOrReadOnly]


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    lookup_url_kwarg = "ticket_pk"
    permission_classes = [IsAdminOrReadOnly]
    
    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        tickets = Ticket.objects.filter(event_id=event_id)
        
        if not event and not tickets:
            raise NotFound()
        
        return tickets
    
    def perform_create(self, serializer):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        serializer.save(event=event)


class LikeViewSet(viewsets.ModelViewSet):
    serializer_class = LikeSerializer
    lookup_url_kwarg = "like_pk"
    permission_classes = [IsAdminOrIsOwnerOrReadOnly]
    
    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        likes = Like.objects.filter(event_id=event_id)
        
        if not event and not likes:
            raise NotFound()
        
        return likes
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
        
    def perform_create(self, serializer):
        user = self.request.user
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        
        try:
            serializer.save(event=event, user=user)
        except IntegrityError:
            raise ValidationError("You have already liked this event.")


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    lookup_url_kwarg = "comment_pk"
    permission_classes = [IsAdminOrIsOwnerOrReadOnly]
    
    def get_queryset(self):
        event_id = self.kwargs["event_pk"]
        event = get_object_or_404(Event, pk=event_id)
        comments = Comment.objects.filter(event_id=event_id)
        
        if not event and not comments:
            raise NotFound()
        
        return comments
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        self.check_object_permissions(request, instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def perform_create(self, serializer):
        event_id = self.kwargs["event_pk"]
        user = self.request.user
        event = get_object_or_404(Event, pk=event_id)
        serializer.save(event=event, user=user)
