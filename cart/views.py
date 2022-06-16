from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from .services.services import add_product_to_cart, get_data_for_add_to_cart, remote_product, get_cart


@require_POST
def cart_add(request, pk):
    """Добавляет товар в корзину"""
    cart, product, form = get_data_for_add_to_cart(request, pk)

    if form.is_valid():
        add_product_to_cart(form, cart, product)

    return redirect('cart:cart_detail')


def cart_remove(request, pk):
    """Удаляет товар из корзины"""
    remote_product(request, pk)

    return redirect('cart:cart_detail')


@login_required(login_url='shop:login')
def cart_detail(request):
    """Представление корзины пользователя"""
    cart = get_cart(request)

    return render(request, 'cart/detail.html', {'cart': cart})
