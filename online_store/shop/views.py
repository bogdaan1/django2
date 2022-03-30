
from django.shortcuts import render, redirect
from .models import Product
from .models import *
from django.contrib.auth.decorators import login_required
from . import forms
from django.db.models import Q


@login_required(login_url='/users/sign_in')
def products_list(request):
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    product_id = request.GET.get('product')
    search_value = request.GET.get('search')

    if product_id:
        product = Product.objects.get(id=product_id)
        cart_item = CartItem.objects.filter(product=product)
        if not cart_item:
            cart_item = CartItem.objects.create(
                customer=request.user,
                product=product,
                quantity=1
            )
            cart_item.save()
            return redirect('shop:products_list')

        for item in cart_item:
            item.quantity += 1
            item.save()

    products = Product.objects.all()
    slides = Slide.objects.all()

    products = products.filter(category=category) if category else products
    products = products.filter(brand=brand) if brand else products
    products = products.filter(
        Q(title__icontains=search_value) |
            Q(description__icontains=search_value)) if search_value else products
        
    return render(request, 'products.html', {'products': products, 'slides': slides})


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(
        request,
        'cart.html',
        {'cart_items': cart_items,
         'total_price': total_price,
         'total_quantity': total_quantity}
    )


def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk).delete()
    return redirect('shop:cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'decrement' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('shop:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop:cart')


def product_detail(request, pk):
    product = Product.objects.get(pk=pk)
    return render(request, 'product_detail.html', {'product': product})


def create_order(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    form = forms.OrderForm(request.POST)

    if request.method == 'POST' and form.is_valid() and cart_items:
        order = Order.objects.create(
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price,
            customer=request.user
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )
        cart_items.delete()
        return redirect('shop:cart')

    return render(request, 'create_order.html', {'cart_items': cart_items,
                                                 'total_price': total_price,
                                                 'total_quantity': total_quantity,
                                                 'form': form})
def rate_product(request, pk):
    product = Product.objects.get(pk=pk)
    reviews = Review.objects.filter(user=request.user)

    if request.method == 'POST':
        form = forms.RateForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('shop:rate_product')
    form = forms.RateForm()
    return render(request, 'rate_product.html',
                      {'form': form, 'product': product, 'reviews': reviews})


def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {'orders': orders_list})
