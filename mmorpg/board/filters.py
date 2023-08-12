from django.forms import DateTimeInput
from django_filters import FilterSet, DateTimeFilter
from .models import *


class ComentFilter(FilterSet):
    added_after = DateTimeFilter(
            field_name='dateCreation',
            lookup_expr='gt',
            widget=DateTimeInput(
                format='%Y-%m-%d',
                attrs={'type':'date'},
            ),
            label=pgettext_lazy('date of creation', 'Posted after')
        )

    class Meta:
        model = Coment
        fields = {
            'author__username': ['contains'],
            'post__title': ['icontains'],
            'accepted': ['exact']
        }