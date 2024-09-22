from api.services.variant import (
    create_variant,
    create_option,
    update_variant,
    update_option,
    delete_variant,
    delete_option,
)
from api.selectors.variant import (
    get_variants,
    get_variant_by_id,
    get_options,
    get_variant_option_by_id,
)
from api.serializers.variant import (
    VariantSerializer,
    VariantOptionSerializer,
    VariantOptionCreateSerializer,
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.permissions import IsAdminOrSeller
from rest_framework.generics import GenericAPIView
from django_filters.rest_framework import DjangoFilterBackend


class VariantListView(APIView):
    """
    List all variants variant.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get(self, request):
        variants = get_variants()
        serializer = VariantSerializer(variants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VariantDetailView(APIView):
    """
    Retrieve variant instance.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get(self, request, variant_id):
        variant = get_variant_by_id(variant_id)
        if variant is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VariantCreateView(APIView):
    """
    Create a variant.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = VariantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        variant = create_variant(serializer.validated_data)
        serializer = VariantSerializer(variant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VariantUpdateView(APIView):
    """
    Update a variant.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, variant_id):
        variant = get_variant_by_id(variant_id)
        if variant is None:
            return Response(
                {"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = VariantSerializer(variant, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        variant = update_variant(variant, serializer.validated_data)
        return Response(VariantSerializer(variant).data, status=status.HTTP_200_OK)


class VariantDeleteView(APIView):
    """
    Delete a variant.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, variant_id):
        variant = get_variant_by_id(variant_id)
        if variant is None:
            return Response(
                {"error": "Variant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_variant(variant)
        return Response(status=status.HTTP_204_NO_CONTENT)


class VariantOptionListView(GenericAPIView):
    """
    List all options.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get_queryset(self):
        return get_options()

    serializer_class = VariantOptionSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["variant"]

    def get(self, request):

        filtered_items = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filtered_items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VariantOptionDetailView(APIView):
    """
    Retrieve option instance.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def get(self, request, option_id):
        option = get_variant_option_by_id(option_id)
        if option is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = VariantOptionSerializer(option)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VariantOptionCreateView(APIView):
    """
    Create an option.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def post(self, request):
        serializer = VariantOptionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        option = create_option(serializer.validated_data)
        return Response(
            VariantOptionSerializer(option).data, status=status.HTTP_201_CREATED
        )


class VariantOptionUpdateView(APIView):
    """
    Update an option.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def patch(self, request, option_id):
        option = get_variant_option_by_id(option_id)
        if option is None:
            return Response(
                {"error": "Option not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = VariantOptionSerializer(option, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        option = update_option(option, serializer.validated_data)
        serializer = VariantOptionSerializer(option)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VariantOptionDeleteView(APIView):
    """
    Delete an option.
    """

    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, option_id):
        option = get_variant_option_by_id(option_id)
        if option is None:
            return Response(
                {"error": "Option not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_option(option)
        return Response(status=status.HTTP_204_NO_CONTENT)
