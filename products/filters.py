from django_filters import rest_framework as filters
from products.models import Product


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter(field_name='price')

    class Meta:
        model = Product
        fields = ['price', 'category']