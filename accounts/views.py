from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db import transaction
from payments.models import Order
from orders.models import OrderItem
from products.models import Products
import logging
from .forms import RegisterForm, LoginForm  # Đảm bảo đã import ở đầu file

logger = logging.getLogger(__name__)


@login_required
def profile(request):
    user_orders = Order.objects.filter(
        user=request.user).order_by('-created_at')
    purchased_products = Products.objects.filter(
        orderitem__order__in=user_orders).distinct()
    return render(request, 'account/profile.html', {
        'orders': user_orders,
        'purchased_products': purchased_products,
    })


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        register_form = RegisterForm()
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(
                    request, 'Tên đăng nhập hoặc mật khẩu không đúng!')
        # Nếu không hợp lệ hoặc sai thông tin, render lại form với lỗi
        return render(request, 'accounts/auth.html', {
            'login_form': login_form,
            'register_form': register_form,
        })
    else:
        login_form = LoginForm()
        register_form = RegisterForm()
    return render(request, 'accounts/auth.html', {
        'login_form': login_form,
        'register_form': register_form,
    })


def register(request):
    if request.method == 'POST':
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            messages.success(
                request, 'Đăng ký thành công, vui lòng đăng nhập!')
            return redirect('accounts:login')
    else:
        register_form = RegisterForm()
    return render(request, 'accounts/register.html', {
        'register_form': register_form,
    })


@login_required
def profile_view(request):
    return render(request, 'account/profile.html')
