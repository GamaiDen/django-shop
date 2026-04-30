"""
Сервисные функции для работы с продуктами.
"""
from django.core.cache import cache
from .models import Product, Category


def get_products_by_category(category_id: int):
    """
    Возвращает список продуктов в указанной категории.
    Результат кешируется на 15 минут.
    """
    cache_key = f"category_{category_id}"
    products = cache.get(cache_key)

    if products is None:
        products = Product.objects.filter(category_id=category_id, is_published=True)
        cache.set(cache_key, list(products), timeout=60 * 15)

    return products


def get_product_detail(product_id: int):
    """
    Возвращает продукт по ID.
    Результат кешируется на 15 минут.
    """
    cache_key = f"product_{product_id}"
    product = cache.get(cache_key)

    if product is None:
        from django.shortcuts import get_object_or_404
        product = get_object_or_404(Product, pk=product_id)
        cache.set(cache_key, product, timeout=60 * 15)

    return product
