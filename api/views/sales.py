from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.services.sales import (
    get_daily_sales_stats,
    get_weekly_sales_stats,
    get_monthly_sales_stats,
)


class DailySalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = request.user
        sales_data = get_daily_sales_stats(seller)
        return Response(sales_data)


class WeeklySalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = request.user
        sales_data = get_weekly_sales_stats(seller)
        return Response(sales_data)


class MonthlySalesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        seller = request.user
        sales_data = get_monthly_sales_stats(seller)
        return Response(sales_data)
