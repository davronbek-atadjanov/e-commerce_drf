from django.urls import path

from products.views import CategoryListView, ProductListView, ProductColorListView, ProductSizeListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("colours/", ProductColorListView.as_view(), name="colours_list"),
    path("sizes/", ProductSizeListView.as_view(), name="sizes_list"),
]

