from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.decorators import api_view, action

from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.viewsets import ModelViewSet

from .models import Category, Tag, Post, Comment, Like
from .permissions import IsAdminPermission, IsAuthorPermission
from .serializers import CategorySerializer, TagSerializer, PostSerializer, CommentSerializer


# class CategoriesListView(APIView):
#     def get(self, request, format=None):
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         categories = serializer.data
#         return Response(categories)


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TagsListView(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# class PostsListView(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
# #
#
# class CreatePostView(CreateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAdminPermission, ]
#
#
# class PostDetails(RetrieveAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#
#
# class UpdatePostView(UpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthorPermission, ]
#
# class DeletePostView(DestroyAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     permission_classes = [IsAuthorPermission, ]


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'slug'
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tags__slug', 'category', 'author']
    search_fields = ['title', 'text', 'tags__title']
    ordering_fields = ['created_at', 'title']

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        post = self.get_object()
        comments = post.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


    @action(['POST'], detail=True)
    def like(self, request, slug=None):
        post = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(post=post, user=user)
            like.is_liked = not like.is_liked
            like.save()
            message = 'liked' if like.is_liked else 'disliked'
        except Like.DoesNotExist:
            Like.objects.create(post=post, user=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    def get_permissions(self):
        if self.action == 'create':
            permissions = [IsAdminPermission]
        elif self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsAuthorPermission]
        elif self.action == 'like':
            permissions = [IsAuthenticated]
        else:
            permissions = []
        return [perm() for perm in permissions]

    def get_serializer_context(self):
        return {'request': self.request, 'action': self.action}

    # def get_serializer_class(self):
    #     if self.action == 'list':
    #         return PostListSerializer
    #     return PostSerializer

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     tags = self.request.query_params.get('tags')
    #     if tags is not None:
    #         tags = tags.split(',')
    #         queryset = queryset.filter(tags__slug__in=tags)
    #     return queryset

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'posts': reverse('post-list', request=request, format=format),
        'categories': reverse('categories-list', request=request, format=format),
        'tags': reverse('tags-list', request=request, format=format)
    })


class CommentCreateView(CreateAPIView):
    queryset = Comment.objects.none()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, ]


# TODO: сделать валидацию данных при создании
# TODO: подключить роутер
# TODO: сделать пагинацию
# TODO: сделать фильтрацию
# TODO: сделать поиск
# TODO: сделать документацию
# TODO: сделать авторицию
# TODO: сделать избранное(лайки)
# TODO: автором поста должен быть пользователь отправляющий запрос

# POST - create
# GET - list, retrieve(details)
# api/v1/post - create, list
# api/v1/post/<id/slug> - details, update, delete

# PUT, PATCH - update
# DELETE - destroy


# 1. Модель клиент-сервер
# 2. Отсутствие состояния(на сервере не хранится информация о состонии клиента), Token
# 3. Кэширование Redis, Memcached
# 4.  Единообразие интерфейса
# 5. Слои
# 6. Код по требованию
