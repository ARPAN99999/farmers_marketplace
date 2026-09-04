from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProductForm
from .models import Product

def product_list(request):
	products = Product.objects.filter(is_available=True, stock__gt=0)
	query = request.GET.get('q', '').strip()
	category = request.GET.get('category', '')
	if query:
		products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))
	if category:
		products = products.filter(category=category)
	return render(request, 'products/list.html', {'products': products, 'query': query, 'category': category, 'categories': Product.CATEGORY_CHOICES})

@login_required
def add_product(request):
	if request.user.profile.role != 'farmer':
		messages.error(request, 'Only farmer accounts can list products.')
		return redirect('products:list')
	form = ProductForm(request.POST or None)
	if request.method == 'POST' and form.is_valid():
		product = form.save(commit=False)
		product.farmer = request.user
		product.save()
		messages.success(request, 'Your product is now listed.')
		return redirect('products:list')
	return render(request, 'products/product_form.html', {'form': form})

@login_required
def add_to_cart(request, product_id):
	product = get_object_or_404(Product, pk=product_id, is_available=True)
	cart = request.session.get('cart', {})
	cart[str(product_id)] = min(cart.get(str(product_id), 0) + 1, product.stock)
	request.session['cart'] = cart
	messages.success(request, f'{product.name} added to your cart.')
	return redirect(request.POST.get('next') or 'products:list')
