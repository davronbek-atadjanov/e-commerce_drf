from django.shortcuts import render
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView

from products.models import Category, Product, ProductColor, ProductSize, ProductReview
from products.serializers import CategoryListSerializer, ProductListSerializer, ProductColorListSerializer, \
    ProductSizeListSerializer, AddReviewToProductSerializer
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


class AddReviewToProductApiView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = AddReviewToProductSerializer

class ProductReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ProductReview.objects.all()
    serializer_class = AddReviewToProductSerializer
    lookup_field = 'id'


class ProductReviewListApiView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = AddReviewToProductSerializer

    def get_queryset(self):
        product_id = self.kwargs.get('product_id')
        return ProductReview.objects.filter(product_id=product_id)


class ProductListByCategoryApiView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        return Product.objects.filter(category_id=category_id)  # Ushbu kategoriy

#
# class

"""
# Bu yerda asosan API View da yozigan viewlar bo'ladi, Yuqoridagi lar bilan bir xil ko'rinishda bo'ladi
class AddReviewToProductApiView(APIView):
    permission_classes = [IsAuthenticated]
    def post (self, request):
        serializer = AddReviewToProductSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            serializer.save(user=user)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(data = serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProductReviewDetailApiView(APIView):
    def get(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        serializer = AddReviewToProductSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def patch(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        serializer = AddReviewToProductSerializer(instance=review, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        serializer = AddReviewToProductSerializer(instance=review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, review_id):
        try:
            get_object_or_404(ProductReview, id=review_id)
        except ObjectDoesNotExist:
            data = {
                "detail": 'Bunday review topilmadi'
            }
            return Response(data, status=status.HTTP_404_NOT_FOUND)
        review = ProductReview.objects.get(id=review_id)
        review.delete()
        data = {
            "message": "O'chirildi"
        }
        return Response(data=data, status=status.HTTP_204_NO_CONTENT)
"""