from django import forms

from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to='media',blank=True, null=True)

    class Meta:
        verbose_name='Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return f'{self.name}'



class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField()

    image = models.ImageField(upload_to='media',blank=True, null=True)

    class Meta:
        verbose_name='Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self):
        return f'{self.name}, {self.category}, {self.pub_date}, {self.price}'