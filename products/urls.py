from django.urls import path

from products.views import CategoryListView, ProductListView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("products", ProductListView.as_view(), name="product_list"),
]

