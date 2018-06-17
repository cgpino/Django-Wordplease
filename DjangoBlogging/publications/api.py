from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from publications.models import Publication
from publications.permissions import PublicationPermissions
from publications.serializers import PublicationListSerializer, PublicationDetailSerializer, NewPublicationSerializer, \
    BlogListSerializer


class PublicationViewSet(ModelViewSet):

    queryset = Publication.objects.all()
    permission_classes = [PublicationPermissions]
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return NewPublicationSerializer
        elif self.action == 'list':
            return PublicationListSerializer
        else:
            return PublicationDetailSerializer

    def perform_create(self, serializer):
        serializer.save(publisher=self.request.user)

    def perform_update(self, serializer):
        serializer.save()


class BlogListAPI(ListAPIView):
    serializer_class = BlogListSerializer

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = ['username']
    ordering_fields = ['username']

    def get_queryset(self):
        return User.objects.all()

class PublicationsUsersAPI(ListAPIView):

    serializer_class = PublicationListSerializer

    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'body']
    ordering_fields = ['created_on']
    ordering = ['-created_on']

    def get_queryset(self):

        # Recuperar de la base de datos el usuario que me piden
        user = get_object_or_404(User, username=self.kwargs.__str__().split('\'')[3])

        # Si el usuario es administrador o está viendo su propio blog, puede ver los post no publicados
        if self.request.user.is_superuser or self.request.user.username == user.username:
            return Publication.objects.filter(publisher=user)
        else:
            return Publication.objects.filter(published=True, publisher=user)