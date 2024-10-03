from django.shortcuts import render, get_object_or_404
from django.views import generic
from unicodedata import category

from shop.models import Category, Product


# Create your views here.
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'objects_list'

    def get_queryset(self):
        return Category.objects.filter()

class ProductListView(generic.ListView):
    model = Product
    context_object_name = 'p_object_list'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(category_id=self.kwargs.get('pk'))
        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_item = Category.objects.get(pk=self.kwargs.get('pk'))
        context_data['category_pk'] = category_item.pk
        context_data['title'] = category_item.name
        return context_data
