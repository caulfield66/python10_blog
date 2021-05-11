from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter

import account
from main.views import CategoriesListView, TagsListView, PostViewSet, api_root, CommentCreateView


router = DefaultRouter()
router.register('posts', PostViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Blog API',
        default_version='v1',
        description='My blog\'s API'
    ), public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    path('api/v1/', include('account.urls')),
    path('', api_root),
    path('api/v1/categories/', CategoriesListView.as_view(), name="categories-list"),
    path('api/v1/tags/', TagsListView.as_view(), name="tags-list"),
    path('api/v1/comments/', CommentCreateView.as_view(), name="create-comment")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
