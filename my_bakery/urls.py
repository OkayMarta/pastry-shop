"""
Конфігурація URL-адрес для проекту my_bakery.

Список `urlpatterns` направляє URL-адреси до відповідних представлень (views).
Для отримання додаткової інформації див.:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Приклади:
Функціональні представлення (Function views)
    1. Імпортуйте: from my_app import views
    2. Додайте URL до urlpatterns:  path('', views.home, name='home')
Класові представлення (Class-based views)
    1. Імпортуйте: from other_app.views import Home
    2. Додайте URL до urlpatterns:  path('', Home.as_view(), name='home')
Включення іншої конфігурації URL-адрес (URLconf)
    1. Імпортуйте функцію include(): from django.urls import include, path
    2. Додайте URL до urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings # Для доступу до налаштувань проекту (наприклад, DEBUG, MEDIA_URL)
from django.conf.urls.static import static # Для обслуговування статичних та медіафайлів у режимі розробки

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shop.urls')),
]

# Додаємо URL-шаблон для медіафайлів тільки якщо DEBUG=True
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)