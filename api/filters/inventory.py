from django_filters.rest_framework import FilterSet

from api.models import Inventory


class InventoryFilter(FilterSet):
    class Meta:
        model = Inventory
        fields = {
            "product": ["exact"],
            "store": ["exact"],
            "stock": ["gt", "lt"],
        }
