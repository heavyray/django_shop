from django.shortcuts import get_object_or_404

from shop.models import Product
from cart.cart import Cart
from cart.forms import CartAddProductForm


def get_product(pk: int) -> Product:
    """Возвращает продукт"""
    return get_object_or_404(Product, id=pk)


def get_cart(request) -> Cart:
    """Возвращает корзину пользователя"""

    return Cart(request)


def get_data_for_add_to_cart(request, pk: int) -> tuple:
    """Возвращает данные для представления добавления товара в корзину"""
    cart = get_cart(request)
    product = get_product(pk)
    form = CartAddProductForm(request.POST)

    return cart, product, form


def add_product_to_cart(form, cart: Cart, product: Product) -> None:
    """Добавляет товар в корзину"""
    cd = form.cleaned_data
    cart.add(
        product=product,
        quantity=cd['quantity'],
        update_quantity=cd['update']
    )


def remote_product(request, pk: int) -> None:
    """Удаляет товар из корзины"""
    cart = get_cart(request)
    product = get_product(pk)
    cart.remove(product)
