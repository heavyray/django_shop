from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import Shop, Product, Status, Profile
from django.urls import reverse
from orders.models import Order, OrderItem


class OrderCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10)
        cls.user = user
        cls.pk = product.id

    def setUp(self):
        self.client.force_login(user=self.user)
        self.get_response = self.client.get(reverse(viewname='orders:order_create'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/order/create/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'orders/order.html')

    def test_permission_denied(self):
        self.client.logout()
        response = self.client.get('/cart/')
        self.assertRedirects(response, '/login/?next=/cart/', status_code=302)

    def test_post_method(self):
        data = {'address': 'test', 'postal_code': 'test', 'city': 'test'}
        self.client.post(reverse(viewname='cart:cart_add', args=[self.pk]))
        response = self.client.post(reverse(viewname='orders:order_create'), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.all().count(), 1)
