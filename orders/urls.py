from django.urls import path
from .views import AddToCartView, UpdateCartItemView, DeleteCartItemView, CartItemListView, OrderCreateView, \
    OrderListView, OrderDetailView, OrderCancelView, OrderDiscountAPIView

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart-items/", CartItemListView.as_view(), name="cart_items"),
    path("cart-items/<int:id>/", UpdateCartItemView.as_view(), name="update_cart_item"),
    path("cart-items/<int:id>/delete/", DeleteCartItemView.as_view(), name="delete_cart_item"),
    path("order-cancel/", OrderCancelView.as_view(), name="order_cancel"),
    path("order-discount/", OrderDiscountAPIView.as_view(), name="order_discount"),
]