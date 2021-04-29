from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


@api_view()
def categories_list(request):
    categories = Category.objects.all()
    print(categories)
    serializer = CategorySerializer(categories, many=True)
    categories = serializer.data
    print(categories)
    return Response(categories)
