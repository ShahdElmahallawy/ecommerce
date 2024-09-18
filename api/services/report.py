from api.selectors.report import get_report_by_id_and_user
from rest_framework.exceptions import ValidationError
from api.models.report import Report


def create_report(user, report_type, rid, message):

    report = Report.objects.create(
        user=user,
        report_type=report_type,
        rid=rid,
        message=message,
    )
    return report
