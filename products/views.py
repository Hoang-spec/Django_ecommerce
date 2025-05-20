from django.shortcuts import render
from rest_framework import generics
from django.http import JsonResponse
from .models import Products
from .serializers import ProductSerializer
from django.db.models import Q  # Import Q objects để tạo truy vấn OR
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

def product_categories(request):
    categories = Products.objects.values_list('type', flat=True).distinct()
    return render(request, 'products/home.html', {'categories': categories})
@csrf_exempt
def product_autocomplete(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        products = Products.objects.filter(name__icontains=query)[:5]
        results = [{'id': p.id, 'name': p.name} for p in products]
    return JsonResponse(results, safe=False)

def product_detail(request, product_id):
    product = get_object_or_404(Products, id=product_id)
    context = {'product': product}
    return render(request, 'products/product_detail.html', context)

def product_search(request):
    query = request.GET.get('q', '')
    products = []
    if query:
        products = Products.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
    return render(request, 'products/search_results.html', {'products': products, 'query': query})
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer

def index(request):
    return  render(request, 'products/home.html')
def product_list_view(request):
    products = Products.objects.all()
    return  render(request, 'products/home.html', {'products': products})
def product_detail(request, pk):
    product = Products.objects.get(pk=pk)
    related_products = Products.objects.filter(type=product.type).exclude(id=product.id)[:10]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


def contact_view(request):
    return render(request, 'orther/contact.html')