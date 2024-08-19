import logging
from api.models.category import Category

logger = logging.getLogger(__name__)


def get_all_categories():
    return Category.objects.all()


def get_category_by_id(pk):
    try:
        category = Category.objects.get(pk=pk)
        return category
    except Category.DoesNotExist:
        logger.error(f"Category with id {pk} not found.")
        return None


def get_products_by_category(category):
    return category.products.all()
