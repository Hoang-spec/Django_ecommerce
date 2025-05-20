from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from products.models import Product
from .models import Review
from .forms import ReviewForm


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    average_rating = Review.get_average_rating(product)
    user_review = None

    if request.user.is_authenticated:
        user_review = Review.objects.filter(
            product=product, user=request.user).first()

    if request.method == 'POST' and request.user.is_authenticated:
        if user_review:
            form = ReviewForm(request.POST, instance=user_review)
        else:
            form = ReviewForm(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(
                request, 'Đánh giá của bạn đã được cập nhật thành công!')
            return redirect('product_detail', product_id=product.id)
        else:
            messages.error(
                request, 'Vui lòng kiểm tra lại thông tin đánh giá.')
    else:
        if user_review:
            form = ReviewForm(instance=user_review)
        else:
            form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'average_rating': average_rating,
        'user_review': user_review,
    }
    return render(request, 'reviews/review_list.html', context)


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id
    review.delete()
    messages.success(request, 'Đánh giá đã được xóa thành công!')
    return redirect('product_detail', product_id=product_id)
