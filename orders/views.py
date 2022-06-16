from django.shortcuts import render

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .services.services import get_cart, get_form_create_order, check_balance_for_purchase, finish_create_order


class OrderCreate(LoginRequiredMixin, View):
    """Представление оформления заказа"""

    def get(self, request):
        cart, form = get_cart(request), get_form_create_order()

        return render(request, 'orders/order.html', {'cart': cart, 'form': form})

    def post(self, request):
        form, cart, total_price, profile = check_balance_for_purchase(
            request=request,
            form=get_form_create_order(request.POST)
        )

        if form.is_valid():
            order = finish_create_order(form, request.user.id, profile, cart, total_price)

            return render(request, 'orders/success.html', {'order': order})

        return render(request, 'orders/order.html', {'cart': cart, 'form': form})
