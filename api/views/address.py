# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from api.serializers.address import AddressSerializer
from api.selectors.address import get_all_addresses_for_user, get_address_by_id
from api.services.address import create_address, update_address, delete_address


class AddressListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = get_all_addresses_for_user(request.user)
        serializer = AddressSerializer(addresses, many=True)
        return Response(serializer.data)


class AddressCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data.copy()
        data["user"] = request.user.id
        serializer = AddressSerializer(data=data)
        if serializer.is_valid():
            address = create_address(serializer.validated_data)
            return Response(
                AddressSerializer(address).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        address = get_address_by_id(request.user, pk)
        serializer = AddressSerializer(address)
        return Response(serializer.data)


class AddressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        serializer = AddressSerializer(data=request.data, partial=True)
        if serializer.is_valid():
            address = update_address(request.user, pk, serializer.validated_data)
            return Response(AddressSerializer(address).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        response = delete_address(request.user, pk)
        return Response(response, status=status.HTTP_204_NO_CONTENT)
