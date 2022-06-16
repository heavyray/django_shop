from django.db import transaction

from shop.models import Profile, Product
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.models import OrderItem, Order


def get_cart(request) -> Cart:
    """Возвращает корзину пользователя"""
    return Cart(request)


def get_form_create_order(data=None) -> OrderCreateForm:
    """Возвращает форму оформления заказа"""
    return OrderCreateForm(data) if data else OrderCreateForm()


def get_profile(user_id: int) -> Profile:
    """Возвращает дополнительную информацию о пользователе"""
    return Profile.objects.only('balance', 'status').get(user_id=user_id)


def check_balance_for_purchase(request, form: OrderCreateForm) -> tuple:
    """Проверяет достаточно ли средств у пользователя для оформления заказа"""
    cart = get_cart(request)

    profile = get_profile(request.user.id)
    total_price = cart.get_total_price()

    if total_price > profile.balance:
        form.add_error(field='address', error='Недостаточно средств на счете для оформления заказа')

    return form, cart, total_price, profile


def finish_create_order(form, user_id, profile, cart, total_price) -> Order:
    """Оформление заказа и создание соответствующих записей в БД"""
    order = form.save(commit=False)
    order.customer_id = user_id

    create_order(
        profile=profile,
        user_id=user_id,
        total_price=total_price,
        cart=cart,
        order=order
    )

    return order


@transaction.atomic
def create_order(profile, user_id, total_price, cart, order) -> None:
    """Транзакция оформления заказа"""
    profile.balance -= total_price
    order.save()

    for item in cart:
        create_order_item(order, item)

    cart.clear()

    check_user_status(profile, user_id)


def create_order_item(order, item) -> None:
    """Создает объекты заказа и списывает товар с остатков"""
    OrderItem.objects.create(order=order,
                             product=item['product'],
                             price=item['price'],
                             quantity=item['quantity'])

    product = Product.objects.only('stock').get(id=item['product'].id)
    product.stock -= item['quantity']
    product.save(update_fields=['stock'])


def check_user_status(profile, user_id) -> None:
    """Обновляет статус пользователя"""
    if profile.status_id == 3:
        return

    orders = Order.objects.prefetch_related('items').filter(customer_id=user_id)

    if sum(order.get_total_cost() for order in orders) >= 5000:
        profile.status_id = 2
    elif sum(order.get_total_cost() for order in orders) >= 50000:
        profile.status_id = 3

    profile.save(update_fields=['balance', 'status'])
