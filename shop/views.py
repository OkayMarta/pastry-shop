# shop/views.py
from django.shortcuts import render, redirect  # Функції для рендерингу шаблонів та перенаправлення
from django.contrib import messages  # Фреймворк для відображення одноразових повідомлень користувачу
from django.core.mail import send_mail  # Функція для надсилання електронних листів
from django.template.loader import render_to_string  # Для рендерингу HTML-шаблону листа в рядок
from django.conf import settings  # Для доступу до налаштувань проекту (наприклад, email адміністратора)
from .models import AssortmentItem, Order  # Імпорт моделей додатку
from .forms import OrderForm  # Імпорт форми замовлення
from django.utils import timezone  # Для роботи з датою та часом
import json  # Для серіалізації даних у формат JSON (для передачі цін на фронтенд)


# Представлення для головної сторінки сайту
def home(request):
    """
    Відображає головну сторінку.
    Вибирає перші 4 товари з асортименту для відображення як бестселери.
    """
    assortment_items = AssortmentItem.objects.all()[:4]  # Отримання перших 4 товарів
    # Рендеринг шаблону home.html з передачею списку товарів у контекст
    return render(request, 'shop/home.html', {'assortment_items': assortment_items})


# Представлення для створення нового замовлення
def order_create(request):
    """
    Обробляє створення нового замовлення.
    При GET-запиті відображає порожню форму (або з попередньо вибраним товаром).
    При POST-запиті валідує дані форми, зберігає замовлення та надсилає email-сповіщення.
    """
    initial_data = {}  # Словник для початкових даних форми (наприклад, попередньо вибраний товар)

    # Перевірка, чи передано ID товару через GET-параметр (наприклад, з кнопки "Замовити" на сторінці товару)
    product_id = request.GET.get('product_id')
    if product_id:
        try:
            # Спроба знайти товар за ID та додати його до початкових даних форми
            product = AssortmentItem.objects.get(pk=product_id)
            initial_data['product'] = product
        except AssortmentItem.DoesNotExist:
            # Якщо товар не знайдено, відобразити повідомлення про помилку
            messages.error(request, 'Обраний товар не знайдено.')

    if request.method == 'POST':  # Обробка POST-запиту (відправка форми)
        form = OrderForm(request.POST)  # Створення екземпляра форми з отриманими даними
        if form.is_valid():  # Перевірка валідності даних форми
            order = form.save(commit=False)  # Створення об'єкта замовлення, але ще не збереження в базу
            order.order_date = timezone.now().date()  # Встановлення поточної дати як дати замовлення
            order.save()  # Збереження об'єкта замовлення в базу даних

            # Підготовка та надсилання email-сповіщення адміністратору про нове замовлення
            subject = 'Нове замовлення!'  # Тема листа
            # Рендеринг HTML-версії листа з шаблону
            html_message = render_to_string('shop/email/order_notification.html', {
                'order': order  # Передача об'єкта замовлення в контекст шаблону листа
            })
            # Створення текстової версії листа (для поштових клієнтів, що не підтримують HTML)
            plain_message = f"""
            Нове замовлення №{order.id}
            Замовник: {order.customer_name}
            Телефон: {order.phone_number}
            Email: {order.email}
            Товар: {order.product.name}
            Кількість: {order.quantity}
            Дата доставки: {order.delivery_date}
            Коментар: {order.comment}
            """
            recipients = [settings.ADMIN_EMAIL]  # Список отримувачів (адреса адміністратора з налаштувань)

            try:
                # Надсилання листа
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=settings.DEFAULT_FROM_EMAIL,  # Адреса відправника з налаштувань
                    recipient_list=recipients,
                    html_message=html_message  # Додавання HTML-версії листа
                )
                # Повідомлення про успішне створення замовлення
                messages.success(request, 'Замовлення успішно створено! Ми зв\'яжемося з вами найближчим часом.')
            except Exception as e:
                # Обробка можливих помилок при надсиланні листа
                # У реальному проекті тут варто додати логування помилки:
                # import logging
                # logger = logging.getLogger(__name__)
                # logger.error(f"Помилка відправки email для замовлення {order.id}: {e}", exc_info=True)
                messages.error(request,
                               f'Сталася помилка при відправці email адміністратору. Будь ласка, спробуйте пізніше або зв\'яжіться з нами напряму.')

            # Перенаправлення на сторінку успішного оформлення замовлення
            return redirect('shop:order_success')
        # Якщо форма невалідна, виконання продовжується, і користувач побачить форму з помилками
    else:  # Обробка GET-запиту (перше відкриття сторінки форми)
        form = OrderForm(initial=initial_data)  # Створення порожньої форми або з початковими даними

    # Підготовка даних про ціни товарів для передачі в JavaScript (для динамічного розрахунку суми)
    assortment_items_prices = {item.id: float(item.price) for item in AssortmentItem.objects.all()}
    assortment_prices_json = json.dumps(assortment_items_prices)  # Серіалізація цін у JSON-рядок

    # Формування контексту для передачі у шаблон
    context = {
        'form': form,  # Об'єкт форми
        'assortment_prices_json': assortment_prices_json  # JSON-рядок з цінами
    }
    # Рендеринг шаблону сторінки оформлення замовлення
    return render(request, 'shop/order_form.html', context)


# Представлення для сторінки, що відображається після успішного створення замовлення
def order_success(request):
    """Відображає сторінку підтвердження успішного замовлення."""
    return render(request, 'shop/order_success.html')


# Представлення для сторінки "Про нас"
def about(request):
    """Відображає сторінку 'Про нас'."""
    return render(request, 'shop/about.html')


# Представлення для сторінки "Асортимент" з можливістю пошуку та фільтрації
def assortment_list(request):
    """
    Відображає список товарів асортименту.
    Підтримує пошук за назвою товару, фільтрацію за ціною та сортування.
    """
    items_query = AssortmentItem.objects.all()  # Починаємо з усіх товарів

    # Отримання параметрів фільтрації та пошуку
    q = request.GET.get('q', '')
    min_price_str = request.GET.get('min_price', '')
    max_price_str = request.GET.get('max_price', '')
    sort_option = request.GET.get('sort', 'default')  # 'default', 'price_asc', 'price_desc'

    # Фільтрація за назвою
    if q:
        items_query = items_query.filter(name__icontains=q)

    # Фільтрація за мінімальною ціною
    if min_price_str:
        try:
            items_query = items_query.filter(price__gte=float(min_price_str))
        except ValueError:
            pass  # Ігнорувати, якщо min_price не є числом

    # Фільтрація за максимальною ціною
    if max_price_str:
        try:
            items_query = items_query.filter(price__lte=float(max_price_str))
        except ValueError:
            pass  # Ігнорувати, якщо max_price не є числом

    # Логіка сортування
    if sort_option == 'price_asc':
        items_query = items_query.order_by('price')
    elif sort_option == 'price_desc':
        items_query = items_query.order_by('-price')
    else: # 'default' або будь-яке інше значення
        items_query = items_query.order_by('pk') # Сортування за порядком додавання (за первинним ключем)

    context = {
        'items': items_query,
        'current_sort': sort_option,
        # Передаємо поточні значення фільтрів, щоб зберегти їх у формі та посиланнях
        'q_value': q,
        'min_price_value': min_price_str,
        'max_price_value': max_price_str,
    }
    return render(request, 'shop/assortment.html', context)