from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import Shop, Product
from orders.models import Order, OrderItem


class OrderAndOrderItemModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='test', password='test')
        order = Order.objects.create(customer=user, address='test', postal_code='test', city='test')
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10)
        cls.order = order
        cls.order_item = OrderItem.objects.create(order=order, product=product, price=product.price, quantity=2)

    # Test OrderItem model

    def test_order_label(self):
        field_label = self.order_item._meta.get_field('order').verbose_name
        self.assertEqual(field_label, 'Order')

    def test_product_label(self):
        field_label = self.order_item._meta.get_field('product').verbose_name
        self.assertEqual(field_label, 'Product')

    def test_price_code_label(self):
        field_label = self.order_item._meta.get_field('price').verbose_name
        self.assertEqual(field_label, 'Price')

    def test_quantity_label(self):
        field_label = self.order_item._meta.get_field('quantity').verbose_name
        self.assertEqual(field_label, 'Count')

    def test_str_method_oi(self):
        self.assertEquals(str(self.order_item), f'{self.order_item.pk}')

    def test_get_cost_method(self):
        self.assertEquals(self.order_item.get_cost(), 2)

    # Test Order model

    def test_customer_label(self):
        field_label = self.order._meta.get_field('customer').verbose_name
        self.assertEqual(field_label, 'Buyer')

    def test_address_label(self):
        field_label = self.order._meta.get_field('address').verbose_name
        self.assertEqual(field_label, 'Address')

    def test_postal_code_label(self):
        field_label = self.order._meta.get_field('postal_code').verbose_name
        self.assertEqual(field_label, 'Postal code')

    def test_city_label(self):
        field_label = self.order._meta.get_field('city').verbose_name
        self.assertEqual(field_label, 'City')

    def test_created_label(self):
        field_label = self.order._meta.get_field('created').verbose_name
        self.assertEqual(field_label, 'Create')

    def test_str_method_o(self):
        self.assertEquals(str(self.order), f'Order {self.order.pk}')

    def test_get_total_cost_method(self):
        self.assertEquals(self.order.get_total_cost(), 2)
