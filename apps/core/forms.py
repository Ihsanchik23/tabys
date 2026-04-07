from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Order, Response, Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'password1', 'password2')


class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('title', 'description', 'budget')
        labels = {
            'title': 'Название заказа',
            'description': 'Описание',
            'budget': 'Бюджет',
        }


class ResponseForm(forms.ModelForm):
    class Meta:
        model = Response
        fields = ('text', 'price')
        labels = {
            'text': 'Текст отклика',
            'price': 'Ваша цена',
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('full_name', 'city', 'about', 'avatar')
        labels = {
            'full_name': 'Полное имя',
            'city': 'Город',
            'about': 'О себе',
            'avatar': 'Аватар',
        }