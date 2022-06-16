from django.urls import path
from .views import MainPage, register_view, LogInView, LogOutView, UserInfoPage, BalanceReplenishment, success,\
    product_detail, BestSellers


app_name = 'shop'

urlpatterns = [
    path('', MainPage.as_view(), name='main_page'),
    path('register/', register_view, name='register'),
    path('login/', LogInView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('info/<int:pk>/', UserInfoPage.as_view(), name='user_info'),
    path('balance/', BalanceReplenishment.as_view(), name='balance'),
    path('success/', success, name='success'),
    path('best_sellers/', BestSellers.as_view(), name='best_sellers'),
    path('<slug:category_slug>/', MainPage.as_view(), name='main_page_by_categories'),
    path('<int:id>/<slug:slug>/', product_detail, name='product_detail'),
]
