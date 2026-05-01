"""
Сервисные функции для работы с продуктами.
"""
from django.core.cache import cache
from django.shortcuts import get_object_or_404
from .models import Product, Category


def get_products_by_category(*, category_id=None, category_slug=None):
    """
    Возвращает категорию и список продуктов.
    Поддерживает поиск по id или slug.
    Результат кешируется на 15 минут.
    """
    if category_id is not None:
        category = get_object_or_404(Category, pk=category_id)
    else:
        category = get_object_or_404(Category, name__iexact=category_slug)

    cache_key = f"category_{category.id}"
    products = cache.get(cache_key)

    if products is None:
        products = list(
            Product.objects.filter(category=category, is_published=True)
        )
        cache.set(cache_key, products, timeout=60 * 15)

    return category, products


def get_product_detail(product_id: int):
    """
    Возвращает продукт по ID.
    Результат кешируется на 15 минут.
    """
    cache_key = f"product_{product_id}"
    product = cache.get(cache_key)

    if product is None:
        product = get_object_or_404(Product, pk=product_id)
        cache.set(cache_key, product, timeout=60 * 15)

    return product
