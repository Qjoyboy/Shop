from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from unicodedata import category

from config import settings
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


'''CRUD для категорий'''

#CreateView for Category
class CategoryCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Category
    fields = ('name',)
    permission_required = "shop.add_category"
    success_url = reverse_lazy('shop:category')


#DetailView for Category
class CategoryDetailView(DetailView):
    model = Category
    template_name = "shop/category_detail.html"

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        if settings.CACHE_ENABLED:
            key = f'product_list_{self.object.pk}'
            product_list = cache.get(key)
            if product_list is None:
                product_list = self.object.product_set.all()
                cache.set(key, product_list)

        else:
            product_list = self.object.product_set.all()

        context_data['product'] = product_list
        return context_data


#UpdateView for Category
class CategoryUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Category
    fields = ('name',)
    permission_required = 'shop.change_category'
    success_url = reverse_lazy('shop:category')
#DeleteView for Category
class CategoryDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Category
    success_url = reverse_lazy('shop:category')

    def test_func(self):
        return self.request.user.is_superuser


#--------------------------------------------------
"""CRUD для продуктов"""

#CreateView for Product
class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    fields = ('name','price','category')
    permission_required = 'shop.add_category'

    def get_success_url(self):
        return reverse('shop:products', args=[self.object.category.pk])

#UpdateView for Product
class ProductUpdateView(LoginRequiredMixin,PermissionRequiredMixin,UpdateView):
    model = Product
    fields = ('name','price','category')
    permission_required = 'shop.change_category'
    def get_success_url(self):
        return reverse('shop:products', args=[self.object.category.pk])

#DetailView for Product
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'

#DeleteView for Product
class ProductDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Product

    def test_func(self):
        return self.request.user.is_superuser

    def get_success_url(self):
        return reverse('shop:products', args=[self.object.category.pk])

