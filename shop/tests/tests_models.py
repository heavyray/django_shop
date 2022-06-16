from django.contrib.auth.models import User
from django.test import TestCase
from ..models import Status, Profile, Shop, Product


class StatusModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.status = Status.objects.create(name='test')

    def test_name_label(self):
        field_label = self.status._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Status')

    def test_str_method(self):
        self.assertEquals(str(self.status), 'test')


class ProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', password='test')
        cls.profile = Profile.objects.create(user=user)

    def test_user_label(self):
        field_label = self.profile._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'User')

    def test_balance_label(self):
        field_label = self.profile._meta.get_field('balance').verbose_name
        self.assertEqual(field_label, 'Balance')

    def test_status_label(self):
        field_label = self.profile._meta.get_field('status').verbose_name
        self.assertEqual(field_label, 'Status')

    def test_str_method(self):
        self.assertEquals(str(self.profile), 'Info about test')


class ShopModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.shop = Shop.objects.create(name='test', description='test')

    def test_name_label(self):
        field_label = self.shop._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_description_label(self):
        field_label = self.shop._meta.get_field('description').verbose_name
        self.assertEqual(field_label, 'Description')

    def test_str_method(self):
        self.assertEquals(str(self.shop), 'test')


class ProductModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(name='test', description='test')
        name = 'test'
        cls.product = Product.objects.create(name=name, price=1, in_shop=shop, stock=10, slug=name)

    def test_name_label(self):
        field_label = self.product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, 'Title')

    def test_price_label(self):
        field_label = self.product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'Price')

    def test_in_shop_label(self):
        field_label = self.product._meta.get_field('in_shop').verbose_name
        self.assertEqual(field_label, 'Shop')

    def test_stock_label(self):
        field_label = self.product._meta.get_field('stock').verbose_name
        self.assertEqual(field_label, 'Stock')

    def test_str_method(self):
        self.assertEquals(str(self.product), 'test')

    def test_get_absolute_url_method(self):
        self.assertEquals(self.product.get_absolute_url(), f'/{self.product.id}/{self.product.slug}/')
