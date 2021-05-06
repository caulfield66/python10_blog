from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import account
from main.views import CategoriesListView, TagsListView, PostViewSet, api_root, CommentCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/categories/', CategoriesListView.as_view(), name='categories-list'),
    path('api/v1/tags/', TagsListView.as_view(), name='tags-list'),
    path('', api_root),
    path('api/v1/posts/', PostViewSet.as_view(
        {'post': 'create', 'get': 'list'}
    ), name='post-list'),
    path('api/v1/posts/<slug:slug>/', PostViewSet.as_view(
        {'put': 'update', 'patch': 'partial_update', 'get': 'retrieve', 'delete': 'destroy' }
    ), name='post-detail'),
    path('api/v1/', include('account.urls')),
    path('api/v1/comments/', CommentCreateView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
