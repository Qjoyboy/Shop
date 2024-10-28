from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from unicodedata import category

from shop.models import Category, Product


# Create your views here.
class CategoryListView(generic.ListView):
    model = Category
    context_object_name = 'objects_list'

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        context_data['title'] = f'Shop - категории товаров'
        return context_data

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
        context_data['title'] = f'Shop - товары'
        return context_data

    """Необходимо переопределить гет саксес урл, потому что реверсе лэйзи не работает"""


'''CRUD без Detail для категорий'''

#CreateView for Category
class CategoryCreateView(CreateView):
    model = Category
    fields = ('name',)
    success_url = reverse_lazy('shop:category')
#UpdateView for Category
class CategoryUpdateView(UpdateView):
    model = Category
    fields = ('name',)
    success_url = reverse_lazy('shop:category')
#DeleteView for Category
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('shop:category')


#--------------------------------------------------
"""CRUD для продуктов"""

#CreateView for Product
class ProductCreateView(CreateView):
    model = Product
    fields = ('name','price','category')
    success_url = reverse_lazy('shop:products')

#UpdateView for Product
class ProductUpdateView(UpdateView):
    model = Product
    fields = ('name','price','category')
    # success_url = reverse_lazy('shop:products')
    def get_success_url(self):
        return reverse('shop:products', args=[self.object.category.pk])

#DetailView for Product
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

#DeleteView for Product
class ProductDeleteView(DeleteView):
    model = Product
    def get_success_url(self):
        return reverse('shop:products', args=[self.object.category.pk])

