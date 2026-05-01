from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from .models import Product
from .forms import ProductForm
from .services import get_products_by_category, get_product_detail


class HomeView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(is_published=True)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'catalog/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_product_detail(pk)


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm('catalog.can_unpublish_product')

    def get_success_url(self):
        cache.delete(f"product_{self.object.pk}")
        return reverse_lazy('product_detail', kwargs={'pk': self.object.pk})


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        obj = self.get_object()
        return obj.owner == self.request.user or self.request.user.has_perm('catalog.can_unpublish_product')

    def form_valid(self, form):
        cache.delete(f"product_{self.object.pk}")
        return super().form_valid(form)


class CategoryProductsView(ListView):
    model = Product
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'

    def get_queryset(self):
        self.category, products = get_products_by_category(
            category_id=self.kwargs.get('category_id'),
            category_slug=self.kwargs.get('category_slug'),
        )
        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ContactsView(TemplateView):
    template_name = 'catalog/contacts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['success'] = self.request.GET.get('success', False)
        return context

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        print(f"📨 {name} ({email}): {message}")
        return HttpResponseRedirect(f"{reverse('contacts')}?success=1")
