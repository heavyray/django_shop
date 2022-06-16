from django.shortcuts import render, redirect

from django.views import View
from django.views.generic import DetailView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import RegisterForm, UpdateBalanceForm, DateChooseForm
from cart.forms import CartAddProductForm
from django.contrib.auth.models import User

from .services.services import \
    get_best_seller, get_product, get_info_about_user, get_products_for_main_page, register_user, balance_up


class MainPage(View):
    """Представление с главной страницей"""

    @staticmethod
    def get(request, category_slug=None):

        page_obj, category, categories = get_products_for_main_page(request, category_slug)

        return render(request,
                      template_name='shop/main_page.html',
                      context={'category': category,
                               'categories': categories,
                               'page_obj': page_obj}
                      )


def product_detail(request, id, slug):

    product = get_product(product_id=id, slug=slug)
    cart_product_form = CartAddProductForm()

    return render(request=request,
                  template_name='shop/detail_product.html',
                  context={'product': product, 'cart_product_form': cart_product_form}
                  )


def register_view(request):
    """Представление с регистрацией пользователя"""

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            register_user(form, request)
            return redirect(to='shop:main_page')

    else:
        form = RegisterForm()

    return render(request,
                  'shop/register.html', context={'form': form}
                  )


class LogInView(LoginView):
    """Представление авторизации пользователя"""
    template_name = 'shop/login.html'


class LogOutView(LogoutView):
    """Представление выхода пользователя из аккаунта"""
    template_name = 'shop/logout.html'


class UserInfoPage(DetailView):
    """Представление с детальной информацией и пользователе"""
    model = User
    template_name = 'shop/user_info.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['other_info'] = get_info_about_user(self.object.id, 'balance', 'status')
        return context


class BalanceReplenishment(LoginRequiredMixin, FormView):
    """Представление пополнения баланса"""
    form_class = UpdateBalanceForm
    template_name = 'shop/balance.html'
    success_url = '/success/'
    login_url = 'shop:login'

    def form_valid(self, form):
        balance_up(user_id=self.request.user.id, count=int(self.request.POST['count']))
        return super().form_valid(form)


def success(request):
    return render(request,
                  template_name='shop/success.html'
                  )


class BestSellers(View):
    """Представление с самым продаваемым товаром за период времени"""

    @staticmethod
    def get(request):
        form = DateChooseForm()
        return render(request, 'shop/best_sellers.html', context={'form': form, 'product': None})

    @staticmethod
    def post(request):
        form = DateChooseForm(request.POST)
        best_seller, count = None, None

        if form.is_valid():
            best_seller, count = get_best_seller(form=form)
            form = DateChooseForm()

        return render(request,
                      'shop/best_sellers.html',
                      context={'form': form, 'product': best_seller, 'count': count}
                      )
