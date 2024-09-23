from rest_framework.permissions import IsAuthenticated
from api.permissions import IsAdminOrSeller
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.store import StoreSerializer, StoreDetailSerializer

from api.services.store import (
    create_store,
    update_store,
    delete_store,
)

from api.selectors.store import (
    get_stores,
    get_store_by_id,
    get_stores_by_seller,
    get_store_by_seller,
)


class StoreListView(APIView):

    def get(self, request):
        stores = get_stores()
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreDetailView(APIView):
    def get(self, request, store_id):
        store = get_store_by_id(store_id)
        serializer = StoreDetailSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreBySellerView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get(self, request):
        stores = get_stores_by_seller(request.user)
        serializer = StoreSerializer(stores, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def post(self, request):
        serializer = StoreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        store = create_store(request.user, serializer.validated_data)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StoreUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def patch(self, request, store_id):
        store = get_store_by_seller(request.user, store_id)
        if not store:
            return Response(
                {"detail": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = StoreSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        store = update_store(store, request.data)
        serializer = StoreSerializer(store)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StoreDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def delete(self, request, store_id):
        store = get_store_by_seller(request.user, store_id)
        if not store:
            return Response(
                {"detail": "Store not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_store(store)
        return Response(status=status.HTTP_204_NO_CONTENT)
