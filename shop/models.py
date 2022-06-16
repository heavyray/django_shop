from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Status(models.Model):
    """Модель статусной системы суммы покупок пользователей"""
    name = models.CharField(
        max_length=20, verbose_name=_('статус'))

    class Meta:
        verbose_name_plural = _('статусы')
        verbose_name = _('статусы')

    def __str__(self) -> str:
        return str(self.name)


class Profile(models.Model):
    """Расширение модели пользователя"""
    user = models.OneToOneField(
        to=User,
        on_delete=models.CASCADE,
        verbose_name=_('пользователь')
    )
    balance = models.IntegerField(
        default=0,
        verbose_name=_('баланс')
    )

    status = models.ForeignKey(
        Status,
        default=1,
        on_delete=models.CASCADE,
        verbose_name=_('статус')
    )

    class Meta:
        verbose_name_plural = _('профили')
        verbose_name = _('профиль')

    def __str__(self) -> str:
        text = _('Инфо о')
        return f'{text} {self.user}'


class Shop(models.Model):
    """Модель магазина"""
    name = models.CharField(
        max_length=20,
        verbose_name=_('название')
    )

    description = models.TextField(
        verbose_name=_('описание')
    )

    class Meta:
        verbose_name_plural = _('магазины')
        verbose_name = _('магазин')

    def __str__(self) -> str:
        return str(self.name)


class Category(models.Model):
    """Модель категории товара"""
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def get_absolute_url(self):
        return reverse('shop:main_page_by_categories', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """Модель товара"""
    category = models.ForeignKey(
        to=Category,
        related_name='products',
        on_delete=models.SET_NULL,
        null=True
    )

    name = models.CharField(
        max_length=100,
        verbose_name=_('название'),
        db_index=True
    )

    description = models.TextField(
        blank=True,
        verbose_name=_('описание')
    )

    image = models.ImageField(
        upload_to='products/%Y/%m/%d',
        blank=True,
        verbose_name=_('фото товара')
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name=_('цена')
    )

    in_shop = models.ForeignKey(
        to=Shop,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name=_('магазин')
    )

    stock = models.PositiveIntegerField(
        verbose_name=_('остаток')
    )

    available = models.BooleanField(
        default=True,
        verbose_name=_('наличие')
    )

    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('создано')
    )

    updated = models.DateTimeField(
        auto_now=True,
        verbose_name=_('обновлено')
    )

    slug = models.SlugField(
        max_length=200,
        db_index=True
    )

    class Meta:
        verbose_name_plural = _('товары')
        verbose_name = _('товар')
        index_together = (('id', 'slug'),)
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.name)

    def get_absolute_url(self) -> str:
        return reverse('shop:product_detail', args=[self.id, self.slug])
