from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from products.models import Product
from .models import CartItem
from .serializers import AddToCartSerializer, UpdateCartItemSerializer


class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AddToCartSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            data = serializer.validated_data
            product = Product.objects.get(id=data.get("product_id"))
            item = CartItem.objects.create(user=request.user, quantity=data.get("quantity"), product=product)
            return Response({"message": "Product added to cart successfully."}, status=status.HTTP_201_CREATED)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e


class UpdateCartItemView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateCartItemSerializer
    queryset = CartItem.objects.all()

    def get_object(self):
        cart_item = self.queryset.get(user=self.request.user, id=self.kwargs.get("pk"))
        return cart_item

# class UpdateCartItemView(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = UpdateCartItemSerializer
#
#     def put(self, request, *args, **kwargs):
#         try:
#             serializer = self.serializer_class(data=request.data)
#             if not serializer.is_valid():
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#             data = serializer.validated_data
#
#             item = CartItem.objects.get(id=kwargs.get("pk"))
#             item.quantity = data.get("quantity")
#             item.save()
#             return Response({"message": "Cart item updated successfully."}, status=status.HTTP_200_OK)
#         except CartItem.DoesNotExist:
#             return Response({"error": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             raise e
