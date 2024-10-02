from django.shortcuts import render
from django.views import generic

from shop.models import Category


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'index.html'
    context_object_name = 'objects_list'

    def get_queryset(self):
        return Category.objects.order_by('name')