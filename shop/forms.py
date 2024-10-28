from django import forms

from shop.models import Product

class ProductForm(forms.Form):
    class Meta:
        model = Product
        fields = ('name','category','price',)