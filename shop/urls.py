# shop/urls.py
from django.urls import path
from . import views

app_name = 'shop'  # Потрібно для правильного звертання через імена маршрутів

urlpatterns = [
    path('', views.home, name='home'),
    path('assortment/', views.assortment_list, name='assortment_list'),  # Тут має бути цей маршрут
    path('about/', views.about, name='about'),
    path('order/', views.order_create, name='order_create'),
    path('order/success/', views.order_success, name='order_success'),
]
