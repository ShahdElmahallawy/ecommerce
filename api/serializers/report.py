from rest_framework import serializers
from api.models.report import Report
from api.models.product import Product
from api.models.order import Order
from api.selectors.product import get_product_by_id
from api.selectors.order import get_order_by_id


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "report_type", "rid", "user", "message"]

    def validate(self, data):
        report_type = data.get("report_type")
        rid = data.get("rid")

        if report_type == "product":
            product = get_product_by_id(rid)
            if product is None:
                raise serializers.ValidationError(
                    "Product with this ID does not exist."
                )

        elif report_type == "order":
            order = get_order_by_id(rid)
            if order is None:
                raise serializers.ValidationError("Order with this ID does not exist.")
        return data
