from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import AssortmentItem, Order
from .forms import OrderForm

def home(request):
    """Головна сторінка"""
    assortment_items = AssortmentItem.objects.all()[:4] # Змінено кількість бестселерів на 4
    return render(request, 'shop/home.html', {'assortment_items': assortment_items})


def assortment_list(request):
    """Список асортименту"""
    items = AssortmentItem.objects.all()
    return render(request, 'shop/assortment.html', {'items': items})


def order_create(request):
    """Створення нового замовлення"""
    initial_data = {}
    product_id = request.GET.get('product_id') # Отримуємо product_id з GET параметрів
    if product_id:
        try:
            product = AssortmentItem.objects.get(pk=product_id)
            initial_data['product'] = product # Встановлюємо початкове значення для поля 'product'
        except AssortmentItem.DoesNotExist:
            messages.error(request, 'Обраний товар не знайдено.') # Обробка помилки, якщо товар не знайдено

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()

            # Відправляємо email ТОЛЬКО адміну (без змін)
            subject = 'Нове замовлення!'
            html_message = render_to_string('shop/email/order_notification.html', {
                'order': order
            })
            plain_message = f"""
            Нове замовлення №{order.id}
            Замовник: {order.customer_name}
            Телефон: {order.phone_number}
            Email: {order.email}
            Товар: {order.product.name} <!- Змінено на order.product.name -->
            Кількість: {order.quantity}
            Дата доставки: {order.delivery_date}
            Коментар: {order.comment}
            """

            recipients = [settings.ADMIN_EMAIL] #  ТОЛЬКО админ

            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=recipients,
                html_message=html_message
            )

            messages.success(request, 'Замовлення успішно створено! Ми зв\'яжемося з вами найближчим часом.')
            return redirect('shop:order_success')
    else:
        form = OrderForm(initial=initial_data) # Передаємо initial_data у форму

    return render(request, 'shop/order_form.html', {'form': form})


def order_success(request):
    """Сторінка успішного створення замовлення"""
    return render(request, 'shop/order_success.html')


def about(request):
    """Сторінка "Про нас" """
    return render(request, 'shop/about.html')