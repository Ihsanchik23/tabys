from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order, Response, Profile
from .forms import RegisterForm, LoginForm, OrderForm, ResponseForm, ProfileForm


def home_view(request):
    latest_orders = Order.objects.select_related('owner').order_by('-created_at')[:6]
    return render(request, 'home.html', {'latest_orders': latest_orders})


def jobs_view(request):
    orders = Order.objects.select_related('owner').order_by('-created_at')
    return render(request, 'jobs.html', {'orders': orders})


def order_detail_view(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    responses = order.responses.select_related('user').order_by('-created_at')

    user_response = None
    can_respond = False

    if request.user.is_authenticated:
        if request.user != order.owner:
            user_response = Response.objects.filter(order=order, user=request.user).first()
            if not user_response:
                can_respond = True

    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user == order.owner:
            messages.error(request, 'Вы не можете откликнуться на свой заказ.')
            return redirect('order_detail', order_id=order.id)

        if Response.objects.filter(order=order, user=request.user).exists():
            messages.error(request, 'Вы уже откликались на этот заказ.')
            return redirect('order_detail', order_id=order.id)

        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.order = order
            response.user = request.user
            response.save()
            messages.success(request, 'Отклик отправлен.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = ResponseForm()

    context = {
        'order': order,
        'responses': responses,
        'form': form,
        'user_response': user_response,
        'can_respond': can_respond,
    }
    return render(request, 'order_detail.html', context)


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('edit_profile')
    else:
        form = RegisterForm()

    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def create_order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.owner = request.user
            order.save()
            messages.success(request, 'Заказ создан.')
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderForm()

    return render(request, 'create_order.html', {'form': form})


@login_required
def edit_profile_view(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль обновлён.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    my_orders = Order.objects.filter(owner=request.user)
    my_responses = Response.objects.filter(user=request.user)

    context = {
        'profile': profile,
        'my_orders': my_orders,
        'my_responses': my_responses,
    }

    return render(request, 'profile.html', context)