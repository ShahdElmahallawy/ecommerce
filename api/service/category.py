import logging
from api.selector.category import get_category_by_id

logger = logging.getLogger(__name__)


def update_category(pk, data):
    category = get_category_by_id(pk)
    if category is None:
        return None

    for field, value in data.items():
        setattr(category, field, value)
    category.save()
    logger.info(f"Category with id {pk} was updated.")
    return category


def delete_category(pk):
    category = get_category_by_id(pk)
    if category is not None:
        category.delete()
        logger.info(f"Category with id {pk} was deleted.")
    else:
        logger.error(f"Failed to delete category: Category with id {pk} not found.")
