import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category
from django.core.files.uploadedfile import SimpleUploadedFile


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(category, db, admin):
    product = Product.objects.create(
        name="product1",
        price=10.00,
        description="A product1",
        count=5,
        category=category,
        currency="EGP",
        created_by=admin,
    )
    print(f"Created Product ID: {product.pk}")
    return product


@pytest.mark.django_db
def test_retrieve_product(api_client_auth, product):
    url = reverse("products:product-detail", kwargs={"pk": product.pk})
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "product1"


@pytest.mark.django_db
def test_create_product(api_admin_auth, category):
    url = reverse("products:create-product")
    image_path = r"api\tests\image.png"

    image = SimpleUploadedFile(
        name="image.png",
        content=open(image_path, "rb").read(),
        content_type="image/png",
    )
    data = {
        "name": "New Product",
        "price": 50.00,
        "description": "A new product description",
        "count": 15,
        "category": category.id,
        "currency": "USD",
        "image": image,
        # 'created_by': authenticated_client,
    }
    response = api_admin_auth.post(url, data, format="multipart")
    assert (
        response.status_code == 201
    ), f"Expected 201 Created, got {response.status_code}. Details: {response.data}"


@pytest.mark.django_db
def test_update_product(api_admin_auth, product):
    url = reverse("products:update-product", kwargs={"pk": product.pk})
    data = {"name": "Updated Product"}
    response = api_admin_auth.put(url, data)
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == "Updated Product"


@pytest.mark.django_db
def test_delete_product(api_admin_auth, product):
    url = reverse("products:delete-product", kwargs={"pk": product.pk})
    print(f"Delete URL: {url}")
    response = api_admin_auth.delete(url)
    print(f"Delete Response: {response.status_code}")
    assert response.status_code == 204
    assert Product.objects.count() == 0
