from django.urls import path
from shop import views

app_name='shop'
urlpatterns = [
    path('',views.CategoryListView.as_view(), name='category'),
    path('products/<int:pk>/', views.ProductListView.as_view(), name='product'),
]