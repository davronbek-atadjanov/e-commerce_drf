from django.urls import path
from .views import AddToCartView, UpdateCartItemView


urlpatterns = [
    path("add-to-cart/", AddToCartView.as_view(), name="add_to_cart"),
    path("cart-items/<int:pk>/", UpdateCartItemView.as_view(), name="update_cart_item"),
]