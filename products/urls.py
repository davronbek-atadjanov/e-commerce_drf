from django.urls import path

from products.views import CategoryListView, ProductListView, ProductColorListView, \
    ProductSizeListView, ProductReviewDetailApiView, AddReviewToProductApiView, \
    ProductReviewListApiView, ProductListByCategoryApiView

urlpatterns = [
    path("categories/", CategoryListView.as_view(), name="category_list"),
    path("products/", ProductListView.as_view(), name="product_list"),
    path("colours/", ProductColorListView.as_view(), name="colours_list"),
    path("sizes/", ProductSizeListView.as_view(), name="sizes_list"),
    path("review/add/", AddReviewToProductApiView.as_view(), name="review"),
    path("review/<int:review_id>", ProductReviewDetailApiView.as_view(), name="detail_review"),
    path("reviews/<int:product_id>", ProductReviewListApiView.as_view(), name="reviews"),
    path('categories/<int:category_id>/products/', ProductListByCategoryApiView.as_view(), name='products_by_category'),

]


