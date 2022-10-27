from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from repairsapi.views import register_user, login_user
from rest_framework import routers
from repairsapi.views import CustomerView


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
]