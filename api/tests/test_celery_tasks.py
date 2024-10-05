import pytest
from unittest.mock import patch, MagicMock
import logging
from api.tasks import send_restock_mails


@pytest.mark.django_db
@patch("api.tasks.send_mail")
@patch("api.tasks.Inventory")
def test_send_restock_mails(mock_product, mock_send_mail, caplog):
    mock_product_instance = MagicMock()
    mock_product_instance.created_by = MagicMock(email="seller@example.com")
    mock_product_instance.supplier = MagicMock(
        name="Supplier X", email="supplier@example.com"
    )
    mock_product_instance.name = "Product X"
    # mock_product_instance.count = 3

    mock_product.objects.select_related.return_value.filter.return_value = [
        mock_product_instance
    ]

    send_restock_mails()

    assert mock_product.objects.select_related.called
    assert mock_send_mail.called

    mock_send_mail.side_effect = Exception("Test exception")
    with caplog.at_level(logging.ERROR):
        send_restock_mails()
    assert mock_product.objects.select_related.called
    assert mock_send_mail.called
    assert "Test exception" in caplog.text
