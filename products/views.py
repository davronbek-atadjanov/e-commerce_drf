from django.shortcuts import render
from rest_framework.generics import ListAPIView

from products.models import Category, Product
from products.serializers import CategoryListSerializer, ProductListSerializer


# Create your views here.


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = None


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
