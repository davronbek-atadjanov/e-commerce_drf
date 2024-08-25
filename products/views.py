from django.shortcuts import render
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from products.models import Category, Product, ProductColor, ProductSize
from products.serializers import CategoryListSerializer, ProductListSerializer, ProductColorListSerializer, \
    ProductSizeListSerializer
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
from .filters import ProductFilter


class CategoryListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    pagination_class = None


# class ProductListView(ListAPIView):
#     queryset = Product.objects.all()
#     serializer_class = ProductListSerializer
#     filter_backends = [DjangoFilterBackend]
#     filterset_class = ProductFilter


class ProductListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', "colors", "sizes"]

    def get_queryset(self):
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price and max_price:
            queryset = self.queryset.filter(price__gte=min_price, price__lte=max_price)
        elif min_price is None and max_price:
            queryset = self.queryset.filter(price__lte=max_price)
        elif max_price is None and min_price:
            queryset = self.queryset.filter(price__gte=min_price)
        else:
            queryset = self.queryset.all()
        return queryset


class ProductColorListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductColor.objects.all()
    serializer_class = ProductColorListSerializer


class ProductSizeListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = ProductSize.objects.all()
    serializer_class = ProductSizeListSerializer