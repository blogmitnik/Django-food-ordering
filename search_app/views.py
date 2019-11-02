from django.shortcuts import render
from shop.models import Product
from django.db.models import Q

def searchResult(request):
	products = None
	query = None
	if 'q' in request.POST:
		query = request.POST.get('q')
		products = Product.objects.all().filter(Q(name__contains=query) | Q(description__contains=query))
	else:
		query = 'Nothing'
	return render(request, 'search.html', {'query':query, 'products':products})