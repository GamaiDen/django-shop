from django.shortcuts import render, get_object_or_404
from .models import Product


def home(request):
    """Главная страница со списком товаров."""
    products = Product.objects.all()
    return render(request, 'catalog/home.html', {'products': products})


def product_detail(request, pk):
    """Страница с детальной информацией о товаре."""
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})


def contacts(request):
    """Страница контактов с формой обратной связи."""
    success = False
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"📨 {name} ({email}): {message}")
        success = True
    return render(request, 'catalog/contacts.html', {'success': success})
