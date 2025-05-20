from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from products.models import Products
from .models import Order, OrderItem
from django.shortcuts import render, redirect
from .models import Address
from django.contrib.auth.decorators import login_required

@login_required
def add_address(request):
    if request.method == 'POST':
        street = request.POST.get('street')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')

        Address.objects.create(
            user=request.user,
            street=street,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone
        )
        return redirect('checkout')  # hoặc trang bạn muốn quay lại
    return render(request, 'payment/add_address.html')

@login_required
def checkout_view(request):
    # Lấy giỏ hàng từ session (giả sử giỏ hàng lưu dưới dạng dictionary)
    cart = request.session.get('cart', {})
    addresses = Address.objects.filter(user=request.user)

    # Kiểm tra kiểu dữ liệu của giỏ hàng
    if not isinstance(cart, dict):
        cart = {}  # Nếu không phải dictionary, khởi tạo lại giỏ hàng

    # Tính tổng số tiền giỏ hàng
    total = 0
    for product_id, quantity in cart.items():
        try:
            product = Products.objects.get(id=product_id)  # Lấy sản phẩm từ DB
            total += product.price * quantity
        except Products.DoesNotExist:
            # Nếu sản phẩm không tồn tại, có thể log lỗi hoặc bỏ qua
            continue

    if request.method == 'POST':
        # Lấy thông tin địa chỉ và số điện thoại từ form
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Tạo một đơn hàng mới và lưu vào DB
        order = Order.objects.create(
            user=request.user,
            address=address,
            phone=phone,
            total_price=total,
            status='Pending',  # Trạng thái đơn hàng có thể là "Pending"
        )

        # Lưu các sản phẩm trong giỏ hàng vào bảng OrderItem
        for product_id, quantity in cart.items():
            try:
                product = Products.objects.get(id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    total_price=product.price * quantity
                )
            except Products.DoesNotExist:
                # Nếu sản phẩm không tồn tại, có thể log lỗi hoặc bỏ qua
                continue

        # Xóa giỏ hàng trong session sau khi thanh toán
        request.session['cart'] = {}

        # Chuyển hướng đến trang thành công
        return render(request, 'payment/susess.html', {'order': order})

    return render(request, 'payment/payment.html', {
        'user': request.user,
        'addresses': addresses,
        'cart': cart,
        'total': total
    })
