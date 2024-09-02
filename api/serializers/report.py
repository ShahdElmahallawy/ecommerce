from rest_framework import serializers
from api.models.report import Report
from api.models.product import Product
from api.models.order import Order


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "report_type", "rid", "user", "message"]

    def validate(self, data):
        report_type = data.get("report_type")
        rid = data.get("rid")

        if report_type == "product":
            if not Product.objects.filter(id=rid).exists():
                raise serializers.ValidationError(
                    "Product with this ID does not exist."
                )
        elif report_type == "order":
            if not Order.objects.filter(id=rid).exists():
                raise serializers.ValidationError("Order with this ID does not exist.")

        return data
