from django.contrib.auth import authenticate
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login as django_login, logout as django_logout
from django.views import View
from django.views.generic import ListView

from django.contrib.auth.models import User

from publications.views import listCategories
from users.forms import LoginForm, RegisterForm


class ListUsers(ListView):

    def get(self, request, **kwargs):
        """
        Muestra el listado de usuarios
        :param **kwargs:
        :param request: objeto HttpRequest
        :return: HttpResponse con respuesta
        """

        # Recuperar usuarios
        users = User.objects.all().order_by('-last_login')

        # Crear contexto
        context = {'users': users,
                   'listCategories': listCategories(request),
                   'navbar': "list-users",}

        # Devolver respuesta usando una plantilla
        return render(request, 'users/home_users.html', context)

class LoginView(View):

    def get(self, request):
        """
        Muestra el formulario de login
        :param request:
        :return:
        """

        form = LoginForm()
        context = {'form': form,
                   'navbar': "login"}
        return render(request, 'users/login.html', context)

    def post(self, request):
        """
        Procesa el login de un usuario
        :param request:
        :return:
        """

        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            # Comprobamos si las credencias son correctas
            user = authenticate(username=username, password=password)
            if user is None:
                # TODO: mostrar mensaje de error al usuario
                messages.error(request, 'Usuario o contraseña incorrecto')
            else:
                # Iniciamos la sesión del usuario (hacemos login del usuario)
                django_login(request, user)
                url = request.GET.get('next', 'home')
                return redirect(url)

        context = {'form': form,
                   'navbar': "login"}

        return render(request, 'users/login.html', context)

class LogoutView(View):

    def get(self,request):
        """
        Hace logout de un usuario
        :param request: objeto HttpRequest
        :return:
        """
        django_logout(request)
        return redirect('login')

class RegisterView(View):

    def get(self, request):
        """
        Muestra el formulario de registro
        :param request:
        :return:
        """

        form = RegisterForm()
        context = {'form': form,
                   'navbar': "register"}
        return render(request, 'users/register.html', context)


    def post(self, request):
        """
        Procesa el formulario de registro
        :param request:
        :return:
        """

        user = User()
        form = RegisterForm(request.POST, instance=user)

        if form.is_valid():
            # Guardar el anuncio
            new_user = form.save()

            # Limpiar el formulario
            form = RegisterForm()

            # Devolvemos un mensaje de OK
            messages.success(request, 'Usuario registrado con éxito')

        context = {'form': form,
                   'navbar': "register"}
        return render(request, 'users/register.html', context)