"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from rest_framework.documentation import include_docs_urls
from rest_framework.permissions import AllowAny
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from users.admin import hidden_admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hidden-admin/', hidden_admin.urls),
    path('api/', include('api.urls')),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('rest-auth/', include('dj_rest_auth.urls')),
    path('rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('docs/', include_docs_urls(
        title='Assessment Tool API Docs',
        permission_classes=[AllowAny]
    )),
]
