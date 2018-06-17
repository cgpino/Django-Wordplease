"""DjangoBlogging URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from DjangoBlogging import settings

from publications.views import HomeView, PublicationDetailView, PublicationFormView, PublicationsUserView, \
    PublicationsCategoryView
from publications.api import PublicationsUsersAPI, PublicationViewSet, BlogListAPI

from users.views import ListUsers, LoginView, LogoutView, RegisterView
from users.api import UserViewSet

router = DefaultRouter()
router.register('publications', PublicationViewSet)
router.register('users', UserViewSet, base_name='users')

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('blogs/<str:name>/', PublicationsUserView.as_view(), name='publications-user'),
    path('blogs/<str:name>/<int:pk>/', PublicationDetailView.as_view(), name='publication-detail-view'),
    path('new-post/', PublicationFormView.as_view(), name='publication-form'),

    path('category/<int:pk>/', PublicationsCategoryView.as_view(), name='publications-category'),

    path('blogs/', ListUsers.as_view(), name='list-users'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', RegisterView.as_view(), name='register'),

    # API URLs
    path('api/v1/', include(router.urls)),

    path('api/v1/blogs/', BlogListAPI.as_view(), name='api-blogs'),
    path('api/v1/blogs/<username>', PublicationsUsersAPI.as_view(), name='api-publications-user')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)