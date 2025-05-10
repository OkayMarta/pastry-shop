# shop/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import AssortmentItem, Order
from .forms import OrderForm
from django.utils import timezone
import json


# Ваші функції home та assortment_list (перша версія)
def home(request):
    assortment_items = AssortmentItem.objects.all()[:4]
    return render(request, 'shop/home.html', {'assortment_items': assortment_items})


def order_create(request):
    initial_data = {}
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            product = AssortmentItem.objects.get(pk=product_id)
            initial_data['product'] = product
        except AssortmentItem.DoesNotExist:
            messages.error(request, 'Обраний товар не знайдено.')

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.order_date = timezone.now().date()

            # Перевірка, чи дата доставки не раніше дати замовлення (поточної дати)
            if order.delivery_date < order.order_date:
                form.add_error('delivery_date', 'Дата доставки не може бути раніше поточної дати.')
                # Якщо є ця помилка, ми НЕ зберігаємо замовлення і НЕ відправляємо email,
                # а переходимо до блоку рендерингу форми з помилками нижче (поза if form.is_valid())
            else:
                # Якщо помилки з датою доставки немає, зберігаємо замовлення і продовжуємо
                order.save()  # Зберігаємо замовлення в базу даних

                subject = 'Нове замовлення!'
                html_message = render_to_string('shop/email/order_notification.html', {
                    'order': order
                })
                plain_message = f"""
                Нове замовлення №{order.id}
                Замовник: {order.customer_name}
                Телефон: {order.phone_number}
                Email: {order.email}
                Товар: {order.product.name if order.product else 'Не вказано'}
                Кількість: {order.quantity}
                Дата доставки: {order.delivery_date}
                Коментар: {order.comment}
                """
                recipients = [settings.ADMIN_EMAIL]

                try:
                    send_mail(
                        subject=subject,
                        message=plain_message,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=recipients,
                        html_message=html_message
                    )
                    messages.success(request, 'Замовлення успішно створено! Ми зв\'яжемося з вами найближчим часом.')
                except Exception as e:
                    messages.error(request, f'Сталася помилка при відправці email адміністратору: {e}')

                return redirect('shop:order_success')
        # Якщо form.is_valid() було False АБО form.add_error було викликано,
        # то код продовжить виконання і дійде до return render нижче,
        # передаючи форму з помилками.
    else:  # GET-запит
        form = OrderForm(initial=initial_data)

    # Цей блок тепер виконується для GET-запитів АБО для POST-запитів, якщо форма невалідна
    # або якщо була додана помилка через form.add_error()
    assortment_items_prices = {item.id: float(item.price) for item in AssortmentItem.objects.all()}
    assortment_prices_json = json.dumps(assortment_items_prices)

    context = {
        'form': form,
        'assortment_prices_json': assortment_prices_json
    }
    return render(request, 'shop/order_form.html', context)


def order_success(request):
    return render(request, 'shop/order_success.html')


def about(request):
    return render(request, 'shop/about.html')


# Ваша друга функція assortment_list
def assortment_list(request):  # Ця функція буде використовуватись, якщо вона визначена пізніше
    items = AssortmentItem.objects.all()
    q = request.GET.get('q', '')
    if q:
        items = items.filter(name__icontains=q)

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)
    return render(request, 'shop/assortment.html', {'items': items})