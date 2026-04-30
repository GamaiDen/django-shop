from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/create/', login_required(views.ProductCreateView.as_view()), name='product_create'),
    path('product/<int:pk>/edit/', login_required(views.ProductUpdateView.as_view()), name='product_update'),
    path('product/<int:pk>/delete/', login_required(views.ProductDeleteView.as_view()), name='product_delete'),
    path('category/<int:category_id>/', views.CategoryProductsView.as_view(), name='category_products'),
    path('contacts/', views.ContactsView.as_view(), name='contacts'),
]
