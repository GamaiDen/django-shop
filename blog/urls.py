from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('blogs/create/', views.BlogCreateView.as_view(), name='blog_create'),
    path('blogs/<int:pk>/edit/', views.BlogUpdateView.as_view(), name='blog_update'),
    path('blogs/<int:pk>/delete/', views.BlogDeleteView.as_view(), name='blog_delete'),
]
