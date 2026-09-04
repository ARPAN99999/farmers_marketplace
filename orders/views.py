from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render
from products.models import Product
from .models import Order, OrderItem

def cart_items(request):
	cart_data = request.session.get('cart', {})
	products = Product.objects.filter(id__in=cart_data.keys(), is_available=True)
	return [(product, cart_data.get(str(product.id), 0)) for product in products]

@login_required
def cart(request):
	items = cart_items(request)
	total = sum((product.price * quantity for product, quantity in items), Decimal('0'))
	return render(request, 'orders/cart.html', {'items': items, 'total': total})

@login_required
def checkout(request):
	items = cart_items(request)
	if not items:
		messages.info(request, 'Your cart is empty.')
		return redirect('products:list')
	if request.method == 'POST':
		address = request.POST.get('delivery_address', '').strip()
		if not address:
			return render(request, 'orders/checkout.html', {'items': items, 'error': 'Please enter a delivery address.'})
		with transaction.atomic():
			order = Order.objects.create(consumer=request.user, delivery_address=address)
			total = Decimal('0')
			for product, quantity in items:
				if quantity > product.stock:
					messages.error(request, f'Not enough stock for {product.name}.')
					return redirect('orders:cart')
				OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
				product.stock -= quantity
				product.save(update_fields=['stock'])
				total += product.price * quantity
			order.total = total
			order.save(update_fields=['total'])
		request.session['cart'] = {}
		return redirect('orders:confirmation', order_id=order.id)
	return render(request, 'orders/checkout.html', {'items': items})

@login_required
def confirmation(request, order_id):
	order = Order.objects.get(id=order_id, consumer=request.user)
	return render(request, 'orders/confirmation.html', {'order': order})

@login_required
def my_orders(request):
	return render(request, 'orders/my_orders.html', {'orders': Order.objects.filter(consumer=request.user)})

@login_required
def farmer_orders(request):
	orders = Order.objects.filter(items__product__farmer=request.user).distinct()
	return render(request, 'orders/farmer_orders.html', {'orders': orders})
