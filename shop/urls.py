from django.urls import path
from shop import views

urlpatterns = [
    path('',views.IndexView.as_view(), name='index')
]