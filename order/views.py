from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from datetime import date

def thanks(request, order_id):
	if order_id:
		customer_order = get_object_or_404(Order, id=order_id)
	return render(request, 'thanks.html', dict(customer_order=customer_order))

@login_required()
def manageOrders(request):
	if request.user.is_authenticated:
		today = date.today().strftime('%Y-%m-%d')
		order_details = Order.objects.filter(created=today)
		total_price = Order.objects.aggregate(total_price=Sum('total'))
	return render(request, 'order/order_list.html', {'order_details':order_details, 'total_price':total_price['total_price']})

@login_required()
def orderHistory(request):
	if request.user.is_authenticated:
		email = str(request.user.email)
		order_details = Order.objects.filter(emailAddress=email)
	return render(request, 'order/order_list.html', {'order_details':order_details})

@login_required()
def viewOrder(request, order_id):
	if request.user.is_authenticated:
		order = Order.objects.get(id=order_id)
		order_items = OrderItem.objects.filter(order=order)
	return render(request, 'order/order_detail.html', dict(order=order, order_items=order_items))

@login_required()
def deleteOrder(request, order_id):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
			email = str(request.user.email)
			order = Order.objects.get(id=order_id, emailAddress=email)
			order.delete()
			messages.success(request, f'Your order #{ order.id } is deleted!')
	return redirect('order:history')

@login_required()
def changeStatus(request, order_id, status_id):
	if request.user.is_authenticated and request.user.is_staff:
		if request.method == 'POST':
			order = Order.objects.get(id=order_id)
			order.status = status_id
			order.save()
			messages.success(request, f'Status of Order #{ order_id } has been set to {order.ORDER_STATUS[order.status][1]}')
	return redirect('order:manage_orders')
