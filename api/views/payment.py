from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.selectors import list_payments, get_payment
from api.serializers.payment import PaymentSerializer
from api.services import update_payment, create_payment, delete_payment


class PaymentListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payments = list_payments(request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        payment = create_payment(serializer.validated_data, request.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_payment(payment_id, request.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_payment(payment_id, request.user)
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        payment = update_payment(serializer.validated_data, payment)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        payment_id = kwargs.get("payment_id")
        payment = get_payment(payment_id, request.user)
        delete_payment(payment)
        return Response(status=status.HTTP_204_NO_CONTENT)
