from django.contrib.auth.models import User
from django.test import TestCase
from shop.models import Shop, Product, Status, Profile
from django.urls import reverse


class CartDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.user = user

    def setUp(self):
        self.client.force_login(user=self.user)
        self.get_response = self.client.get(reverse(viewname='cart:cart_detail'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'cart/detail.html')

    def test_permission_denied(self):
        self.client.logout()
        response = self.client.get('/cart/')
        self.assertRedirects(response, '/login/?next=/cart/', status_code=302)


class CartAddViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10)
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.pk = product.id
        cls.user = user

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_cart_add_post(self):
        self.client.force_login(user=self.user)
        response = self.client.post(reverse(viewname='cart:cart_add', args=[self.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))


class CartRemoveViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10)
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.pk = product.id
        cls.user = user

    def setUp(self):
        self.client.force_login(user=self.user)

    def test_cart_remove_post(self):
        self.client.force_login(user=self.user)
        self.client.post(reverse(viewname='cart:cart_add', args=[self.pk]))
        response = self.client.post(reverse(viewname='cart:cart_remove', args=[self.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('cart:cart_detail'))
