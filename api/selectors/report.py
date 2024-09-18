from api.models.report import Report


def get_user_reports(user):
    return Report.objects.filter(user=user).select_related("user")


def get_report_by_id_and_user(report_id, user):
    return Report.objects.filter(id=report_id, user=user).select_related("user").first()
