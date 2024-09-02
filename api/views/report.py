from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.serializers.report import ReportSerializer

from api.services.report import create_report
from api.selectors.report import get_user_reports, get_report_by_id_and_user


class ReportListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        reports = get_user_reports(request.user)
        serializer = ReportSerializer(reports, many=True)
        return Response(serializer.data)


class ReportCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        report = create_report(
            user=request.user,
            report_type=data.get("report_type"),
            rid=data.get("rid"),
            message=data.get("message"),
        )
        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        report = get_report_by_id_and_user(pk, request.user)
        if not report:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ReportSerializer(report)
        return Response(serializer.data)
