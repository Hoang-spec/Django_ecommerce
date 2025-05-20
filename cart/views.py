from django.shortcuts import render, redirect, get_object_or_404
from products.models import Products
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from .models import Coupon
from .forms import CouponApplyForm


@require_POST
def coupon_apply(request):
    now = timezone.now()
    form = CouponApplyForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(
                code__iexact=code,
                valid_from__lte=now,
                valid_to__gte=now,
                active=True
            )
            request.session['coupon_id'] = coupon.id
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None
    return redirect('cart:view_cart')


def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart:view_cart')


def coupon_remove(request):
    request.session['coupon_id'] = None  # Xóa coupon khỏi session
    return redirect('cart:view_cart')  # Chuyển hướng về giỏ hàng


def add_to_cart(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    cart = request.session.get('cart', {})

    if str(product_id) in cart:
        cart[str(product_id)] += 1
    else:
        cart[str(product_id)] = 1

    request.session['cart'] = cart
    return redirect('cart:view_cart')


def view_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total = 0

    # Tính toán giỏ hàng như cũ
    for product_id, quantity in cart.items():
        product = Products.objects.get(id=product_id)
        item_total = product.price * quantity
        total += item_total
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'item_total': item_total
        })

    coupon_id = request.session.get('coupon_id')
    coupon = None
    discount = 0
    total_after_discount = total

    if coupon_id:
        try:
            coupon = Coupon.objects.get(id=coupon_id)
            if coupon.is_valid():  # Kiểm tra coupon còn hiệu lực
                discount = total * coupon.discount / 100
                total_after_discount = total - discount
        except Coupon.DoesNotExist:
            request.session['coupon_id'] = None

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total': total,
        'coupon': coupon,
        'discount': discount,
        'total_after_discount': total_after_discount
    })


def increase_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        cart[product_id_str] += 1
        request.session['cart'] = cart

    return redirect('cart:view_cart')


def decrease_quantity(request, product_id):
    cart = request.session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart:
        if cart[product_id_str] > 1:
            cart[product_id_str] -= 1
        else:
            del cart[product_id_str]
        request.session['cart'] = cart

    return redirect('cart:view_cart')
