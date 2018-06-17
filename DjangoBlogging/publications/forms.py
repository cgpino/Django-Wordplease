from django.forms import ModelForm
from django.core.exceptions import ValidationError

from publications.models import Publication


class PublicationForm(ModelForm):

    class Meta:
        model = Publication
        fields = '__all__'
        exclude = ['publisher']

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image is not None and 'image' not in image.content_type:
            raise ValidationError('La imagen no es válida')
        return image