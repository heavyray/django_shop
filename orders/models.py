from django.db import models

from django.contrib.auth.models import User
from shop.models import Product

from django.utils.translation import gettext_lazy as _


class Order(models.Model):
    """Модель заказа"""

    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name=_('покупатель')
    )

    address = models.CharField(
        max_length=250,
        verbose_name=_('адрес')
    )

    postal_code = models.CharField(
        max_length=20,
        verbose_name=_('почтовый индекс')
    )

    city = models.CharField(
        max_length=100,
        verbose_name=_('город')
    )

    created = models.DateField(
        auto_now_add=True,
        verbose_name=_('создан')
    )

    class Meta:
        verbose_name = _('заказ')
        verbose_name_plural = _('заказы')

    def __str__(self) -> str:
        text = _('Заказ')
        return f'{text} {self.pk}'

    def get_total_cost(self) -> int:
        """Метод возвращает сумму заказа"""
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    """Модель товара в составе заказа"""

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name=_('заказ')
    )

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='order_items',
        verbose_name=_('товар')
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('цена')
    )

    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name=_('количество')
    )

    class Meta:
        verbose_name = _('заказанный товар')
        verbose_name_plural = _('заказанные товары')

    def __str__(self) -> str:
        return str(self.pk)

    def get_cost(self) -> int:
        """Метод возвращает полную стоимость товара, с учетом его количества в заказе"""
        return self.price * self.quantity
