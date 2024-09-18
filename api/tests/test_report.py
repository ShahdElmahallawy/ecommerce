import pytest
from api.models.report import Report

from api.serializers.report import ReportSerializer

from api.models.user import User

from api.selectors.report import get_user_reports, get_report_by_id_and_user

from api.services.report import create_report

from django.urls import reverse
from rest_framework import status


# test for the model
@pytest.mark.django_db
def test_report_creation(user, product):
    report = Report.objects.create(
        user=user, report_type="product", rid=product.id, message="Test message"
    )
    assert report.report_type == "product"
    assert report.rid == product.id
    assert report.message == "Test message"


# test for serializer
@pytest.mark.django_db
def test_report_serializer(user, product):
    report = Report.objects.create(
        user=user, report_type="product", rid=product.id, message="Test message"
    )
    serializer = ReportSerializer(report)
    data = serializer.data
    assert data["report_type"] == "product"
    assert data["rid"] == product.id
    assert data["message"] == "Test message"
    assert data["user"] == user.id


# test selector
@pytest.mark.django_db
def test_get_user_reports(user, product):
    report = Report.objects.create(
        user=user, report_type="product", rid=product.id, message="Test message"
    )
    reports = get_user_reports(user)
    assert reports.count() == 1
    assert reports.first() == report


@pytest.mark.django_db
def test_get_report_by_id_and_user(user, product):
    report = Report.objects.create(
        user=user, report_type="product", rid=product.id, message="Test message"
    )
    found_report = get_report_by_id_and_user(report.id, user)
    assert found_report == report

    other_user = User.objects.create_user(
        email="other@example.com", name="Other User", password="password"
    )
    assert get_report_by_id_and_user(report.id, other_user) is None


# test services
@pytest.mark.django_db
def test_create_report(user, order):
    report = create_report(
        user=user, report_type="order", rid=order.id, message="New message"
    )
    assert report.report_type == "order"
    assert report.rid == order.id
    assert report.message == "New message"


# tests views
@pytest.mark.django_db
def test_list_reports(api_client_auth, user, product):
    Report.objects.create(
        user=user, report_type="product", rid=product.id, message="Test message"
    )

    url = reverse("report-list")
    response = api_client_auth.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_retrieve_report(api_client_auth, user):
    report = Report.objects.create(
        user=user, report_type="product", rid=1, message="Test message"
    )
    url = reverse("report-detail", kwargs={"pk": report.id})
    response = api_client_auth.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["message"] == report.message
