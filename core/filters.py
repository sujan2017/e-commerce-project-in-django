import django_filters
from .models import Order


class OrderFilter(django_filters.FilterSet):

    start_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="gte"
    )

    end_date = django_filters.DateFilter(
        field_name="created_at",
        lookup_expr="lte"
    )

    min_price = django_filters.NumberFilter(
        field_name="total_price",
        lookup_expr="gte"
    )

    max_price = django_filters.NumberFilter(
        field_name="total_price",
        lookup_expr="lte"
    )

    class Meta:
        model = Order
        fields = ["status"]