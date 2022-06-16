from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class RegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    first_name = forms.CharField(
        max_length=30,
        label=_('Имя')
    )

    last_name = forms.CharField(
        max_length=30,
        label=_('Фамилия')
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class UpdateBalanceForm(forms.Form):
    """Форма для пополнения баланса"""
    count = forms.IntegerField(label=_('Сумма'))


class DateInput(forms.DateInput):
    input_type = 'date'


class DateChooseForm(forms.Form):
    """Форма выбора интервала дат"""
    start = forms.DateField(
        widget=DateInput,
        label=_('С')
    )

    finish = forms.DateField(
        widget=DateInput,
        label=_('по')
    )

    def clean(self):
        """Метод проверяет что дата начала выборки не позднее даты окончания"""
        cleaned_data = super(DateChooseForm, self).clean()

        if cleaned_data.get('start') > cleaned_data.get('finish'):
            raise forms.ValidationError(message='Первая дата должна быть раньше второй')
