from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from api.services.supplier import create_supplier, update_supplier, delete_supplier
from api.selectors.supplier import get_all_suppliers, get_supplier_by_id
from rest_framework.permissions import IsAdminUser
from api.serializers.supplier import SupplierSerializer
from logging import getLogger

logger = getLogger(__name__)


class SupplierCreateView(APIView):
    """
    API view to create a supplier"""

    permission_classes = [IsAdminUser]

    def post(self, request):
        logger.info("Creating a supplier")
        serializer = SupplierSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        supplier = create_supplier(serializer.validated_data)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SupplierUpdateView(APIView):
    """
    API view to update a supplier"""

    permission_classes = [IsAdminUser]

    def patch(self, request, supplier_id):
        logger.info("Updating a supplier")
        serializer = SupplierSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        supplier = update_supplier(supplier_id, serializer.validated_data)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data)


class SupplierDeleteView(APIView):
    """
    API view to delete a supplier"""

    permission_classes = [IsAdminUser]

    def delete(self, request, supplier_id):
        logger.info("Deleting a supplier")
        delete_supplier(supplier_id)
        return Response(status=status.HTTP_204_NO_CONTENT)


class SupplierListView(APIView):
    """
    API view to get all suppliers"""

    def get(self, request):
        logger.info("Getting all suppliers")
        suppliers = get_all_suppliers()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SupplierDetailView(APIView):
    """
    API view to get a supplier"""

    def get(self, request, supplier_id):
        logger.info("Getting a supplier")
        supplier = get_supplier_by_id(supplier_id)
        serializer = SupplierSerializer(supplier)
        return Response(serializer.data, status=status.HTTP_200_OK)
