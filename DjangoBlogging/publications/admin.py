from django.contrib import admin
from django.contrib.admin import register
from django.utils.safestring import mark_safe
from publications.models import Category, Publication

admin.site.register(Category)

@register(Publication)
class PublicationAdmin(admin.ModelAdmin):

    autocomplete_fields = ['publisher']
    list_display = ['image_html', 'title', 'publisher_name', 'published']
    list_filter = ['categories']
    search_fields = ['name', 'price', 'publisher__first_name', 'publisher__last_name', 'publisher__username']

    def publisher_name(self, publication):
        return '{0} {1}'.format(publication.publisher.first_name, publication.publisher.last_name)

    publisher_name.short_description = 'Publisher\'s name'
    publisher_name.admin_order_field = 'publisher__first_name'

    def image_html(self, publication):
        return mark_safe('<img src="{0}" alt="{1}" title="{2}" width="100">'.format(publication.image.url, publication.title, publication.title))

    image_html.short_description = 'Image'
    image_html.admin_order_field = 'image'

    readonly_fields = ['created_on', 'image_html']

    fieldsets = [
        [None, {
            'fields': ['title', 'image', 'image_html', 'publisher']
        }],
        ['Content', {
            'fields': ['introductory_text', 'body']
        }],
        ['Topics', {
            'fields': ['categories']
        }],
        ['Publish data', {
            'fields': ['published']
        }]
    ]