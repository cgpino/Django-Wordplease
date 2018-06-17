from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import ListView
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator, InvalidPage, EmptyPage, PageNotAnInteger

from publications.forms import PublicationForm
from publications.models import Category, Publication
from django.contrib.auth.models import User

class HomeView(ListView):

    def get(self, request, **kwargs):
        """
        Muestra el listado de las últimas publicaciones
        :param **kwargs:
        :param request: objeto HttpRequest
        :return: HttpResponse con respuesta
        """

        # Recuperar publicaciones
        publications = Publication.objects.filter(published=True).order_by('-created_on')

        paginator = Paginator(publications, 3)
        page = request.GET.get('page')
        try:
            publications = paginator.page(page)
        except PageNotAnInteger:
            publications = paginator.page(1)
        except EmptyPage:
            publications = paginator.page(paginator.num_pages)

        # Crear contexto
        context = {'publications': publications,
                   'listCategories': listCategories(request),
                   'navbar': "home"}

        # Listado general de publicaciones
        messages.info(request, 'General')

        # Devolver respuesta usando una plantilla
        return render(request, 'publications/home.html', context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subtitle'] = 'General'
        return context


class PublicationsUserView(View):

    def get(self, request, name):
        """
        Muestra el listado de publicaciones del usuario en concreto
        :param request: objeto HttpRequest
        :param pk: identificador del usuario
        :return: HttpResponse con respuesta
        """

        # Recuperar de la base de datos el usuario que me piden
        try:
            user = User.objects.select_related().get(username=name)
        except User.DoesNotExist:
            # Si no existe el usuario, devolvemos un 404
            return HttpResponse('No existe el usuario que buscas')

        # Se obtienen todas las publicaciones del usuario
        publications = user.publications.filter(published=True).order_by('-created_on')

        paginator = Paginator(publications, 3)
        page = request.GET.get('page')
        try:
            publications = paginator.page(page)
        except PageNotAnInteger:
            publications = paginator.page(1)
        except EmptyPage:
            publications = paginator.page(paginator.num_pages)

        # Crear contexto
        context = {'publications': publications,
                   'listCategories': listCategories(request),
                   'navbar': "publications-user"}

        # Listado de publicaciones de un usuario
        messages.info(request, 'Publicador: ' + str(user.username))

        # Devolver respuesta usando una plantilla
        return render(request, 'publications/home.html', context)

class PublicationsCategoryView(View):

    def get(self, request, pk):
        """
        Muestra el listado de publicaciones de la categoría en concreto
        :param request: objeto HttpRequest
        :param pk: identificador de la categoría
        :return: HttpResponse con respuesta
        """

        # Recuperar de la base de datos el usuario que me piden
        try:
            category = Category.objects.select_related().get(pk=pk)
        except Category.DoesNotExist:
            # Si no existe el usuario, devolvemos un 404
            return HttpResponse('No existe la categoría que buscas')

        # Se obtienen todas las publicaciones de la categoría
        publications = category.publications.filter(published=True).order_by('-created_on')

        paginator = Paginator(publications, 3)
        page = request.GET.get('page')
        try:
            publications = paginator.page(page)
        except PageNotAnInteger:
            publications = paginator.page(1)
        except EmptyPage:
            publications = paginator.page(paginator.num_pages)

        # Crear contexto
        context = {'publications': publications,
                   'listCategories': listCategories(request),
                   'navbar': "home"}

        # Listado de publicaciones de una categoría
        messages.info(request, 'Categoría: ' + str(category.name))

        # Devolver respuesta usando una plantilla
        return render(request, 'publications/home.html', context)


class PublicationDetailView(View):

    def get(self, request, name, pk):
        """
        Muestra el detalle de una publicación
        :param request: objeto HttpRequest
        :param pk: identificador de la publicación
        :return: HttpResponse con la respuesta
        """

        # Recuperar de la base de datos la publicación que me piden
        try:
            publication = Publication.objects.select_related().get(pk=pk)
        except Publication.DoesNotExist:
            # Si no existe el anuncio, devolvemos un 404
            return HttpResponse('No existe la publicación que buscas')

        if not publication.published:
            return HttpResponse('La publicación no está activada')

        # Se comprueba si la publicación coincide con el publicador
        if publication.publisher.username != name:
            return HttpResponse('La publicación no se corresponde con el publicador')


        # Crear contexto
        context = {'publication': publication,
                   'listCategories': listCategories(request),
                   'navbar': "home"}

        # Devolver respuesta usando una plantilla

        return render(request, 'publications/home_detail.html', context)

@method_decorator(login_required, name='dispatch')
class PublicationFormView(View):

        def get(self, request):
                """
                Muestra el formulario
                :param request: objeto HttpRequest
                :return: HttpResponse con la respuesta
                """

                form = PublicationForm()
                context = {'form': form,
                           'navbar': "publication-form"}
                return render(request, 'publications/publication_form.html', context)

        def post(self, request):
                """
                Procesa el formulario
                :param request: objeto HttpRequest
                :return: HttpResponse con la respuesta
                """

                publication = Publication()
                publication.publisher = request.user

                form = PublicationForm(request.POST, request.FILES, instance=publication)
                if form.is_valid():
                        # Guardar el anuncio
                        new_publication = form.save()

                        # Limpiar el formulario
                        form = PublicationForm()

                        # Devolvemos un mensaje de OK
                        messages.success(request, 'Publicación creada correctamente')

                context = {'form': form,
                           'navbar': "publication-form"}
                return render(request, 'publications/publication_form.html', context)

def listCategories(request):

    return Category.objects.all()