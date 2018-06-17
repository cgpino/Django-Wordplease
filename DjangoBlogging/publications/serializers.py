from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from publications.models import Publication


class PublicationListSerializer(ModelSerializer):

    class Meta:

        model = Publication
        fields = ['id', 'title', 'image', 'introductory_text', 'created_on']


class NewPublicationSerializer(ModelSerializer):

    class Meta:

        model = Publication
        fields = ['title', 'introductory_text', 'body', 'image', 'categories', 'published']


class PublicationDetailSerializer(ModelSerializer):

    class Meta:

        model = Publication
        fields = '__all__'

# Devuelve la URL de un usuario
def get_blog_url(self):
    return "/blogs/" + str(self.username)


class BlogListSerializer(ModelSerializer):

    User.add_to_class('get_blog_url', get_blog_url)

    url = serializers.URLField(source='get_blog_url')

    class Meta:

        model = User
        fields = ['username', 'url']