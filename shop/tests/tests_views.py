import datetime
from django.contrib.auth.models import User
from django.db import connection
from django.test import TestCase
from django.urls import reverse

from ..models import Shop, Product, Status, Profile
from orders.models import Order, OrderItem
from django.test.utils import CaptureQueriesContext


class MainPageViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(name='test', description='test')
        for product_num in range(13):
            Product.objects.create(name='test %s' % product_num, price=1, in_shop=shop, stock=10, slug='test')

    def setUp(self):
        self.get_response = self.client.get(reverse(viewname='shop:main_page'))

    def test_view_url_exist_at_desired_location(self):
        with CaptureQueriesContext(connection) as queries:
            response = self.client.get('')
            self.assertEqual(7, len(queries))
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/main_page.html')

    def test_pagination_is_seven(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTrue('page_obj' in self.get_response.context)
        self.assertTrue(self.get_response.context['page_obj'])
        self.assertTrue(len(self.get_response.context['page_obj']) == 7)

    def test_lists_all_products(self):
        response = self.client.get(reverse('shop:main_page') + '?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('page_obj' in response.context)
        self.assertTrue(response.context['page_obj'])
        self.assertTrue(len(response.context['page_obj']) == 6)


class ProductDetailViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10, slug='test')
        cls.id = product.id
        cls.slug = product.slug

    def setUp(self):
        self.get_response = self.client.get(reverse(viewname='shop:product_detail', args=[self.id, self.slug]))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f'/{self.id}/{self.slug}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/detail_product.html')


class RegisterViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        cls.page_name = reverse(viewname='shop:register')
        cls.user = {
            'username': 'username',
            'first_name': 'Test',
            'last_name': 'Test',
            'password1': 'TestPass12',
            'password2': 'TestPass12'
        }
        cls.user_short_password = {
            'username': 'username',
            'first_name': 'Test',
            'last_name': 'Test',
            'password1': 'Test',
            'password2': 'Test'
        }
        cls.user_different_passwords = {
            'username': 'username',
            'first_name': 'Test',
            'last_name': 'Test',
            'password1': 'TestPass12',
            'password2': 'TestPass15'
        }

    def setUp(self):
        self.get_response = self.client.get(self.page_name)

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/register.html')

    def test_can_register_user(self):
        response = self.client.post(self.page_name, self.user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(User.objects.all().count(), 1)
        self.assertEqual(User.objects.get(id=1).username, 'username')

    def test_cant_register(self):
        response = self.client.post(self.page_name, self.user_short_password)
        self.assertNotEqual(response.status_code, 302)
        response = self.client.post(self.page_name, self.user_different_passwords)
        self.assertNotEqual(response.status_code, 302)

    def test_redirect_after_register(self):
        response = self.client.post(self.page_name, self.user)
        self.assertRedirects(response, reverse('shop:main_page'))

    def test_authenticated_after_register(self):
        self.client.post(self.page_name, self.user)
        response = self.client.get(self.page_name)
        self.assertTrue(response.context['user'].is_authenticated)


class UserInfoViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.pk = user.id

    def setUp(self):
        self.get_response = self.client.get(reverse('shop:user_info', args=[self.pk]))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get(f'/info/{self.pk}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/user_info.html')

    def test_view_use_correct_context(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTrue('other_info' in self.get_response.context)


class BalanceReplenishmentViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.user = user
        cls.pk = user.id

    def setUp(self):
        self.client.force_login(user=self.user)
        self.get_response = self.client.get(reverse('shop:balance'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/balance/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/balance.html')

    def test_hase_perm_to_view_page(self):
        self.client.logout()
        response = self.client.get(reverse('shop:balance'))
        self.assertRedirects(response, '/login/?next=/balance/', status_code=302)

    def test_form_valid(self):
        response = self.client.post(path='/balance/', data={'count': 500})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Profile.objects.get(user_id=self.pk).balance, 500)


class SuccessViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        cls.user = user

    def setUp(self):
        self.client.force_login(user=self.user)
        self.get_response = self.client.get(reverse('shop:success'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/success/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/success.html')


class BestSellerViewTest(TestCase):

    def setUp(self):
        self.get_response = self.client.get(reverse('shop:best_sellers'))

    def test_view_url_exist_at_desired_location(self):
        response = self.client.get('/best_sellers/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.assertEqual(self.get_response.status_code, 200)

    def test_view_use_correct_template(self):
        self.assertEqual(self.get_response.status_code, 200)
        self.assertTemplateUsed(self.get_response, 'shop/best_sellers.html')

    def test_post_method(self):
        Status.objects.create(name='test')
        user = User.objects.create_user(username='test', first_name='f_name', last_name='l_name')
        Profile.objects.create(user=user)
        shop = Shop.objects.create(name='test', description='test')
        product = Product.objects.create(name='test', price=1, in_shop=shop, stock=10)
        order = Order.objects.create(customer=user, address='test', postal_code='test', city='test')
        OrderItem.objects.create(order=order, product=product, price=1)

        response = self.client.post(path='/best_sellers/', data={
            'start': datetime.date.today(), 'finish': datetime.date.today()
        })
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['product'])
        self.assertEqual(response.context['product'].name, 'test')
