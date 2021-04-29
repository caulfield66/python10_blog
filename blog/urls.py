
from django.contrib import admin
from django.urls import path

from main.views import categories_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories', categories_list)
]
