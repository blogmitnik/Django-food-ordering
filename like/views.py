from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Like
from shop.models import Product
from django.contrib import messages
from django.http import HttpResponseRedirect

def like_or_unlike_item(request, product_slug):
	if request.user.is_authenticated:
		user = request.user.id
		try:
			product = Product.objects.get(slug=product_slug)
		except Exception as e:
			raise e
		like_product = Like.objects.filter(user_id=user, product_id=product)
		if like_product.exists():
			like_product.delete()
			messages.warning(request, f'You\'ve unliked {product.name}!')
		else:
			like_item = Like.objects.create(user_id=user, product_id=product.id)
			like_item.save()
			messages.warning(request, f'You\'ve liked {product.name}!')
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		return redirect('signin')