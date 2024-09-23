from api.services.inventory import create_inventory, update_inventory, delete_inventory
from api.selectors.inventory import (
    get_inventory_by_id,
    get_inventory_by_id_and_seller,
    get_inventory_by_seller,
)
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from api.serializers.inventory import InventorySerializer, InventoryCreateSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrSeller
from api.filters.inventory import InventoryFilter


class InventoryListView(GenericAPIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get_queryset(self):
        return get_inventory_by_seller(self.request.user)

    serializer_class = InventorySerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    ordering_fields = ["stock"]
    filterset_class = InventoryFilter

    def get(self, request):

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryDetailView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get(self, request, inventory_id):
        inventory = get_inventory_by_id(inventory_id)
        if not inventory:
            return Response(
                {"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def post(self, request):
        serializer = InventoryCreateSerializer(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        inventory = create_inventory(request.user, serializer.validated_data)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class InventoryUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def patch(self, request, inventory_id):
        inventory = get_inventory_by_id_and_seller(inventory_id, request.user)
        if not inventory:
            return Response(
                {"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = InventorySerializer(inventory, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        inventory = update_inventory(inventory, serializer.validated_data)
        serializer = InventorySerializer(inventory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InventoryDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def delete(self, request, inventory_id):
        inventory = get_inventory_by_id_and_seller(inventory_id, request.user)
        if not inventory:
            return Response(
                {"error": "Inventory not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_inventory(inventory)
        return Response(status=status.HTTP_204_NO_CONTENT)
