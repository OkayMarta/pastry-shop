# shop/urls.py
from django.urls import path # Функція для визначення URL-шаблонів
from . import views          # Імпорт представлень (views) з поточного додатку (shop)

# Визначення простору імен для URL-адрес цього додатку.
# Дозволяє уникнути конфліктів імен URL-адрес між різними додатками
# та використовувати конструкції типу {% url 'shop:home' %} у шаблонах.
app_name = 'shop'

# Список URL-шаблонів для додатку 'shop'
urlpatterns = [
    # Головна сторінка сайту (кореневий URL)
    path('', views.home, name='home'), 
    # Сторінка "Асортимент"
    path('assortment/', views.assortment_list, name='assortment_list'),
    # Сторінка "Про нас"
    path('about/', views.about, name='about'),
    # Сторінка створення замовлення
    path('order/', views.order_create, name='order_create'),
    # Сторінка успішного оформлення замовлення
    path('order/success/', views.order_success, name='order_success'),
]