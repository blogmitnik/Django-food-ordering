from django.shortcuts import render, redirect, get_object_or_404
from shop.models import Product
from .models import Cart, CartItem
from order.models import Order, OrderItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from shop.views import sendEmail

def _cart_id(request):
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	return cart

@login_required()
def clear_cart(request):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	cart_items = CartItem.objects.filter(cart=cart)
	cart_items.delete()
	messages.success(request, f'Your shopping cart is now cleared!')
	return redirect('cart:cart_detail')

@login_required()
def add_cart(request, product_id):
	if request.method == "POST":
		product = Product.objects.get(id=product_id)
		if product.can_be_order(request.user):
			try:
				cart = Cart.objects.get(cart_id=_cart_id(request))
			except Cart.DoesNotExist:
				cart = Cart.objects.create(
					cart_id=_cart_id(request)
				)
				cart.save()
			try:
				cart_item = CartItem.objects.get(product=product, cart=cart)
				if cart_item.quantity < cart_item.product.stock:
					cart_item.quantity += 1
				cart_item.save()
			except CartItem.DoesNotExist:
				cart_item = CartItem.objects.create(
					product=product, 
					quantity=request.POST['item_qty'],
					cart=cart,
					memo=request.POST['memo']
				)
				cart_item.save()
		else:
			messages.warning(request, f'Oops! You have no privilege to order this item!')
			return redirect('shop:product_detail', product.category.slug, product.slug)
	return redirect('cart:cart_detail')

@login_required()
def cart_remove(request, product_id):
	if request.method == "POST":
		cart = Cart.objects.get(cart_id=_cart_id(request))
		product = get_object_or_404(Product, id=product_id)
		cart_item = CartItem.objects.get(product=product, cart=cart)
		if cart_item.quantity > 1:
			cart_item.quantity -= 1
			cart_item.save()
		else:
			cart_item.delete()
	return redirect('cart:cart_detail')

@login_required()
def full_remove(request, product_id):
	cart = Cart.objects.get(cart_id=_cart_id(request))
	product = get_object_or_404(Product, id=product_id)
	cart_item = CartItem.objects.get(product=product, cart=cart)
	cart_item.delete()
	return redirect('cart:cart_detail')

@login_required()
def cart_detail(request, total=0, counter=0, cart_items=None):
	try:
		cart = Cart.objects.get(cart_id=_cart_id(request))
		cart_items = CartItem.objects.filter(cart=cart, active=True)
		for cart_item in cart_items:
			total += (cart_item.product.price * cart_item.quantity)
			counter += cart_item.quantity
	except ObjectDoesNotExist:
		pass

	if request.method == "POST":
		orderPlace = request.POST['order_place']
		if total > 30:
			messages.warning(request, f'Your order price is over $30. Please remove something!')
			return redirect('cart:cart_detail')
		else:
			email = request.user.email
			shippingName = request.user.first_name + ' ' + request.user.last_name
			
			"""creating the order"""
			try:
				order_details = Order.objects.create(
					total = total,
					emailAddress = request.user.email, 
					shippingName = shippingName,
					location = orderPlace,
				)
				order_details.save()
				for order_item in cart_items:
					oi = OrderItem.objects.create(
						product = order_item.product.name, 
						quantity = order_item.quantity,
						price = order_item.product.price, 
						order = order_details,
						memo = order_item.memo
					)
					oi.save()
					"""Reduce stock when order is placed or saved"""
					products = Product.objects.get(id=order_item.product.id)
					products.stock = int(order_item.product.stock - order_item.quantity)
					products.save()
					"""Remove order item from shopping cart"""
					order_item.delete()
				
				try:
					"""Send order email to the customer"""
					sendEmail(order_details.id)
					print('Order email has been sent to the Customer!')
				except IOError as e:
					return e

				return redirect('order:thanks', order_details.id)
			except ObjectDoesNotExist:
				pass
	return render(request, 'cart.html', dict(cart_items=cart_items, total=total, counter=counter))

