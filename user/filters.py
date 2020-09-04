from itertools import chain

from django.db.models import Q
from django.db.models.query import QuerySet
from django_filters import rest_framework as filters

from user.models import CustomUser


class UserFilter(filters.FilterSet):
    search = filters.CharFilter(field_name="search", method="filter_search")

    def filter_search(self, queryset: QuerySet, name: str, value: str) -> QuerySet:
        name, last_name, *_ = chain(value.split(" ", 1), [""])

        user_by_full_name = Q(first_name__icontains=name) & Q(last_name__icontains=last_name)
        user_by_last_name = Q(last_name__icontains=name)
        user_by_google_drive_spreadsheet_id = Q(
            google_drive_spreadsheet_id=value
        )

        result_queryset = queryset.filter(
            user_by_full_name | user_by_last_name | user_by_google_drive_spreadsheet_id
        )

        return result_queryset

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name',
                  'google_drive_spreadsheet_id', 'search')
