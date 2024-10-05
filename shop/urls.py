from django.urls import path
from shop import views

app_name = 'shop'
urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category'),
    path('category/create/', views.CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>', views.CategoryDeleteView.as_view(), name='category_delete'),

    path('products/<int:pk>/', views.ProductListView.as_view(), name='products'),
    path('product/create/', views.ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', views.ProductUpdateView.as_view(), name='product_update'),
    path('product/detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='product_delete'),
]
