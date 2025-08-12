# bjf_project/store/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import (
    Product, Category, Post, ContactMessage, Order, OrderItem, 
    Banner, ProductVariation, ProductImage, Testimonial, ActionButton,
    AboutPage, JobPosting
)
from django.views.decorators.http import require_POST
import json

def home(request):
    featured_products = Product.objects.filter(is_available=True, is_featured=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    banners = Banner.objects.filter(is_active=True)
    latest_posts = Post.objects.order_by('-published_date')[:3]
    testimonials = Testimonial.objects.filter(is_active=True).order_by('order')[:3]
    # Lấy 3 tin tuyển dụng mới nhất
    latest_jobs = JobPosting.objects.filter(is_active=True).order_by('-published_date')[:3]
    
    context = {
        'products': featured_products,
        'categories': categories,
        'banners': banners,
        'latest_posts': latest_posts,
        'testimonials': testimonials,
        'latest_jobs': latest_jobs,
    }
    return render(request, 'store/index.html', context)

def about_us(request):
    # Lấy đối tượng trang About Us (vì là singleton nên chỉ có 1)
    about_page_content = AboutPage.objects.get()
    context = {
        'about_page': about_page_content
    }
    return render(request, 'store/about.html', context)

def product_list(request):
    products = Product.objects.filter(is_available=True)
    categories = Category.objects.all()
    context = {
        'products': products,
        'categories': categories,
    }
    return render(request, 'store/product_list.html', context)
    
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_available=True)
    related_products = Product.objects.filter(category=product.category, is_available=True).exclude(id=product.id)[:4]
    
    variations = product.variations.all()
    grouped_variations = {}
    for variation in variations:
        variation_type_display = variation.get_variation_type_display()
        if variation_type_display not in grouped_variations:
            grouped_variations[variation_type_display] = []
        grouped_variations[variation_type_display].append(variation)

    images = product.images.all()

    context = {
        'product': product,
        'related_products': related_products,
        'grouped_variations': grouped_variations,
        'images': images,
    }
    return render(request, 'store/product_detail.html', context)

def post_list(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'store/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        'post': post
    }
    return render(request, 'store/post_detail.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message_content = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message_content)
        messages.success(request, 'Cảm ơn bạn! Tin nhắn của bạn đã được gửi thành công.')
        return redirect('store:contact')
    return render(request, 'store/contact.html')

@require_POST
def add_to_cart(request):
    product_id = request.POST.get('product_id')
    quantity = int(request.POST.get('quantity', 1))
    product = get_object_or_404(Product, id=product_id)
    cart = request.session.get('cart', {})
    
    base_price = product.sale_price if product.sale_price else product.price

    variation_price_change = 0
    selected_variations = {}
    for key, value in request.POST.items():
        if key.startswith('variation_'):
            try:
                variation = ProductVariation.objects.get(id=value)
                variation_price_change += variation.price_change
                selected_variations[key.replace('variation_', '')] = variation.variation_name
            except ProductVariation.DoesNotExist:
                pass
    
    final_price = base_price + variation_price_change
    main_image = product.images.filter(is_main=True).first()

    variation_key = '_'.join([f"{k}-{v}" for k, v in sorted(selected_variations.items())])
    cart_item_key = f"{product_id}-{variation_key}"

    if cart_item_key in cart:
        cart[cart_item_key]['quantity'] += quantity
    else:
        cart[cart_item_key] = {
            'product_id': product_id,
            'name': product.name,
            'price': str(final_price),
            'quantity': quantity,
            'image_url': main_image.image.url if main_image else '',
            'variations': selected_variations,
        }
    
    request.session['cart'] = cart
    messages.success(request, f'Đã thêm "{product.name}" vào giỏ hàng.')
    return redirect(request.META.get('HTTP_REFERER', 'store:product_list'))

def cart_detail(request):
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0
    for product_key, item in cart.items():
        total_item_price = int(item['quantity']) * float(item['price'])
        cart_items.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'image_url': item['image_url'],
            'total_price': total_item_price,
            'variations': item.get('variations', {})
        })
        total_price += total_item_price
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'store/cart_detail.html', context)

def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    
    keys_to_delete = [key for key in cart if key.startswith(f"{product_id}-")]
    for key in keys_to_delete:
        del cart[key]

    request.session['cart'] = cart
    messages.success(request, 'Đã xóa sản phẩm khỏi giỏ hàng.')
    return redirect('store:cart_detail')

def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('store:home')
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        email = request.POST.get('email')
        note = request.POST.get('note')
        total_price = 0
        for item in cart.values():
            total_price += int(item['quantity']) * float(item['price'])
        order = Order.objects.create(full_name=full_name, phone_number=phone_number, address=address, email=email, note=note, total_amount=total_price)
        for product_key, item_data in cart.items():
            product_id = item_data['product_id']
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(order=order, product=product, price=float(item_data['price']), quantity=int(item_data['quantity']))
        del request.session['cart']
        messages.success(request, 'Đặt hàng thành công! Chúng tôi sẽ liên hệ với bạn sớm nhất.')
        return redirect('store:home')
    cart_items = []
    total_price = 0
    for product_key, item in cart.items():
        total_item_price = int(item['quantity']) * float(item['price'])
        cart_items.append({
            'product_id': item['product_id'],
            'name': item['name'],
            'price': float(item['price']),
            'quantity': item['quantity'],
            'total_price': total_item_price,
            'variations': item.get('variations', {})
        })
        total_price += total_item_price
    context = {'cart_items': cart_items, 'total_price': total_price}
    return render(request, 'store/checkout.html', context)

def recruitment(request):
    job_postings = JobPosting.objects.filter(is_active=True)
    context = {
        'job_postings': job_postings
    }
    return render(request, 'store/recruitment.html', context)

def job_detail(request, slug):
    job = get_object_or_404(JobPosting, slug=slug, is_active=True)
    context = {
        'job': job
    }
    return render(request, 'store/job_detail.html', context)