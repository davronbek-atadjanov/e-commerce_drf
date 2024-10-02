from functools import total_ordering

from django.db.models import Q
from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.filters import SearchFilter
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView, CreateAPIView, RetrieveAPIView, \
    get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from accounts.models import UserAddress
from products.models import Product
from .models import CartItem, Order, Discount
from .serializers import AddToCartSerializer, UpdateCartItemSerializer, CartItemListSerializer, OrderCreateSerializer, \
    OrderListSerializer, OrderDetailSerializer, OrderDiscountSerializer


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
        cart_item = self.queryset.get(user=self.request.user, id=self.kwargs.get("id"))
        return cart_item


class DeleteCartItemView(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CartItem.objects.all()
    lookup_field = 'id'
    serializer_class = UpdateCartItemSerializer


class CartItemListView(ListAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderCreateView(CreateAPIView):
   queryset = Order.objects.all()
   serializer_class = OrderCreateSerializer
   permission_classes = [IsAuthenticated]

   def create(self, request, *args, **kwargs):
       try:
           serializer = self.serializer_class(data=request.data)
           if not serializer.is_valid():
               return Response(data={"message":"invalid_data"}, status=status.HTTP_400_BAD_REQUEST)
           address = UserAddress.objects.get(id=serializer.validated_data.get('user_address'))
           cart_items = CartItem.objects.filter(id__in=serializer.validated_data.get('cart_items'))
           total_price = sum([item.product.price for item in cart_items])
           order = Order.objects.create(user=request.user, address=address, total_price=total_price)
           return Response({"message": "Order created successfully.", "result":order.id}, status=status.HTTP_201_CREATED)

       except UserAddress.DoesNotExist:
           return Response(data={"message":"user_address does not exist"}, status=status.HTTP_404_NOT_FOUND)
       except Exception as e:
           raise e


class OrderListView(ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['status', 'payment_status']
    search_fields = ['payment_method']

    def get_queryset(self):
        search_param = self.request.query_params.get('search')
        filtered_queryset = self.filter_queryset(self.queryset)
        if search_param:
            items_ads = CartItem.objects.filter(product__name__contains=search_param).values_list('id', flat=True)
            return filtered_queryset.filter(items__id__in=list(items_ads))
        return filtered_queryset


class OrderDetailView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]


    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, id=kwargs.get("pk"))
        if order.status == Order.OrderStatus.CANCELLED:
            order.status = Order.OrderStatus.CANCELLED
            order.save()
            return Response(data={"message": "Order cancelled successfully."}, status=status.HTTP_200_OK)
        return Response(data={"message": "Order cannot be cancelled"}, status=status.HTTP_400_BAD_REQUEST)


class OrderDiscountAPIView(APIView):
    serializer_class = OrderDiscountSerializer

    def post(self, request, *args, **kwargs):
        try:
            serializer = self.serializer_class(data=request.data)
            if not serializer.is_valid():
                return Response(data={"message":"invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            order = get_object_or_404(Order, id=serializer.validated_data.get("order_id"))
            discount = Discount.objects.get(id=serializer.validated_data.get("discount_code"))

            if order.discount is not None:
                return Response(data={"message":"Discount already applied."}, status=status.HTTP_400_BAD_REQUEST)
            order.discount = discount
            discount.max_limit -= 1
            order.total_price -= order.total_price * discount.percent / 100
            discount.save()
            order.save()
            return Response(data={"message":"Discount applied successfully."}, status=status.HTTP_200_OK)

        except Discount.DoesNotExist:
            return Response(data={"message":"Discount does not exist"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            raise e


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
