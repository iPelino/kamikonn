import django_filters

from apps.events.models import Event


class EventFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name="category__slug", lookup_expr="exact")
    university = django_filters.CharFilter(
        field_name="universities__short_name", lookup_expr="iexact"
    )

    start_date_after = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="gte")
    start_date_before = django_filters.DateTimeFilter(field_name="start_time", lookup_expr="lte")

    is_virtual = django_filters.BooleanFilter(field_name="is_virtual")
    status = django_filters.CharFilter(field_name="status")

    class Meta:
        model = Event
        fields = [
            "category",
            "university",
            "start_date_after",
            "start_date_before",
            "is_virtual",
            "status",
        ]
