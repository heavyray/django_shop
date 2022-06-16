from typing import Tuple, Optional

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from ..models import Product, Profile, Category
from orders.models import Order


def get_products_for_main_page(request, category_slug: Optional[str]):
    """Возвращает либо все товары, либо товары с заданной категорией с пагинацией"""
    category = None

    categories = Category.objects.all()
    products = Product.objects.select_related('in_shop').filter(available=True).all()

    if category_slug:
        category = get_object_or_404(klass=Category, slug=category_slug)
        products = products.filter(category=category)

    paginator = Paginator(products, 7)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj, category, categories


def get_product(product_id: int, slug: str) -> Product:
    """Возвращает объект товара из БД"""
    return get_object_or_404(klass=Product, id=product_id, slug=slug, available=True)


def register_user(form, request) -> None:
    """Регистрирует и авторизует пользователя"""
    user = form.save()
    Profile.objects.create(user=user)
    username = form.cleaned_data.get('username')
    raw_password = form.cleaned_data.get('password1')
    user = authenticate(username=username, password=raw_password)
    login(request, user)


def get_info_about_user(user_id: int, *args) -> Profile:
    """Возвращает дополнительную информацию о пользователе"""
    return Profile.objects.only(*args).get(user_id=user_id)


def get_best_seller(form) -> Tuple[Product, int]:
    """Возвращает самый покупаемый товар за период времени и его количество"""

    products = {}
    form = form.data.dict()
    start = form.get('start')
    finish = form.get('finish')
    orders = Order.objects.prefetch_related('items').exclude(created__lt=start).exclude(created__gt=finish)

    for order in orders:
        for item in order.items.all():
            products[item.product.id] = products.get(item.product.id, 0) + item.quantity

    if products:
        product_id = max(products, key=products.get)
        best_seller = Product.objects.only('id', 'name').get(id=product_id)
        count = products[product_id]

        return best_seller, count


def balance_up(user_id: int, count: int) -> None:
    """Пополнение баланса"""
    profile = get_info_about_user(user_id, 'balance')
    profile.balance += count
    profile.save(update_fields=['balance'])
