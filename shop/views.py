from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import  method_decorator
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from .models import Place, Category, Product
from django.contrib.auth.models import Group, User
from .forms import SignUpForm, CountableMessageForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.template.loader import get_template
from django.core.mail import EmailMessage, send_mail
from order.models import Order, OrderItem
from cart.models import Cart, CartItem
from like.models import Like
from django.views.generic import FormView, TemplateView, ListView, DetailView
from django.db.models import Q

class HomeView(TemplateView):
	template_name = 'shop/home.html'

	#@method_decorator(login_required(login_url=reverse_lazy('login')))

	def get(self, request, *args, **kwargs):
		context = self.get_context_data(**kwargs)
		context['places'] = Place.objects.all() 
		context['popular_products'] = Product.objects.filter(available=True).order_by('-star')[:6]
		if request.user.is_authenticated:
			cart = request.session.session_key
			if not cart:
				cart = request.session.create()
			if not Cart.objects.filter(cart_id=cart).exists():
				cart = Cart.objects.create(cart_id=cart)
				cart.save()
			else:
				cart = Cart.objects.get(cart_id=cart)
			context['cart_items']  = CartItem.objects.filter(cart_id=cart.id)
		return self.render_to_response(context)

def SelectPlace(request):
	place_list = Place.objects.all()
	return render(request, 'shop/choice_place.html', {'place_list':place_list})

@login_required()
def selectDefault(request, place_id):
	if request.method == 'POST':
		restaurant_id = request.POST['restaurant']
		restaurant_name = request.POST['restaurant_name']
		place_name = request.POST['place_name']
		restaurant = Category.objects.filter(~Q(id=restaurant_id)).filter(place_id=place_id)
		restaurant.update(select=0)
		restaurant_selected = Category.objects.filter(id=restaurant_id, place_id=place_id)
		restaurant_selected.update(select=1)
		messages.success(request, f'Restaurant has been set to {restaurant_name} for { place_name }')
	return redirect('shop:restaurants', place_name)

def shopRestaurants(request, place_slug=None):
	restaurant_list = None
	if place_slug != None:
		place = Place.objects.get(slug=place_slug)
		restaurant_list = Category.objects.filter(place=place)
	return render(request, 'shop/restaurants.html', {'place':place, 'restaurant_list':restaurant_list})

def allProdCat(request, c_slug=None, filter_by=None, sort_by=None):
	c_page = None
	products_list = None
	places = Place.objects.all() 
	if c_slug != None:
		c_page = get_object_or_404(Category, slug=c_slug)
		if filter_by != None and filter_by == 'hot':
			products_list = Product.objects.filter(category=c_page, available=True, star__gte=3).order_by('-star')
		elif filter_by != None and filter_by == 'new':
			products_list = Product.objects.filter(category=c_page, available=True).order_by('-created')
			p_ids = [p.id for p in products_list if p.was_new_arrival()]
			products_list = products_list.filter(id__in=p_ids)
		elif filter_by != None and filter_by == 'liked':
			liked_items = Like.objects.filter(user_id=request.user.id)
			liked_items_pids = [liked_item.product_id for liked_item in liked_items]
			products_list = Product.objects.filter(category=c_page, available=True, id__in=liked_items_pids)
		else:
			products_list = Product.objects.filter(category=c_page, available=True)
	else:
		if filter_by != None and filter_by == 'hot':
			products_list = Product.objects.filter(available=True, star__gte=3).order_by('-star')
		elif filter_by != None and filter_by == 'new':
			products_list = Product.objects.filter(available=True).order_by('-created')
			p_ids = [p.id for p in products_list if p.was_new_arrival()]
			products_list = products_list.filter(id__in=p_ids)
		elif filter_by != None and filter_by == 'liked':
			liked_items = Like.objects.filter(user_id=request.user.id)
			liked_items_pids = [liked_item.product_id for liked_item in liked_items]
			products_list = Product.objects.filter(available=True, id__in=liked_items_pids)
		else:
			products_list = Product.objects.filter(available=True)

	if sort_by != None and sort_by == 'price':
		products_list = sorted(products_list, key=lambda product:product.price, reverse=False)

	paginator = Paginator(products_list, 30)
	try:
		page = int(request.GET.get('page', '1'))
	except:
		page = 1
	try:
		products = paginator.page(page)
	except (EmptyPage, InvalidPage):
		products = paginator.page(paginator.num_pages)

	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	if not Cart.objects.filter(cart_id=cart).exists():
		cart = Cart.objects.create(cart_id=cart)
		cart.save()
	else:
		cart = Cart.objects.get(cart_id=cart)
	cart_items  = CartItem.objects.filter(cart_id=cart.id)
	return render(request, 'shop/category.html', {'category':c_page, 'products':products, 'cart_items':cart_items, 'places':places})

@login_required()
def ProdCatDetail(request, c_slug, product_slug):
	try:
		product = Product.objects.get(category__slug=c_slug, slug=product_slug)
	except Exception as e:
		raise e
	cart = request.session.session_key
	if not cart:
		cart = request.session.create()
	if not Cart.objects.filter(cart_id=cart).exists():
		cart = Cart.objects.create(cart_id=cart)
		cart.save()
	else:
		cart = Cart.objects.get(cart_id=cart)
	cart_items  = CartItem.objects.filter(cart_id=cart.id)
	form = CountableMessageForm()
	return render(request, 'shop/product.html', {'product':product, 'cart_items':cart_items, 'form':form})

def signupView(request):
	if request.method == 'POST':
		print(request.POST)
		form = SignUpForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			signup_user = User.objects.get(username=username)
			customer_group = Group.objects.get(name='Customer')
			customer_group.user_set.add(signup_user)
			messages.success(request, f'Your account was successfully created! Please sign in.')
			return redirect('signin')
	else: # Access web page with HTTP GET method
		print('something went wrong!')
		form = SignUpForm()
	return render(request, 'accounts/signup.html', {'form':form})

def signinView(request):
	if request.method == 'POST':
		form = AuthenticationForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.success(request, f'Hello, { username }!')
				return redirect('/')
			else:
				return redirect('signup')
	else: # Access web page with HTTP GET method
		form = AuthenticationForm()

	return render(request, 'accounts/signin.html', {'form':form})

def signoutView(request):
	logout(request)
	return redirect('signin')

def sendEmail(order_id):
	transaction = Order.objects.get(id=order_id)
	order_items = OrderItem.objects.filter(order=transaction)
	try:
		subject = 'Django Cart - New order #{}'.format(transaction.id)
		to = ['{}'.format(transaction.emailAddress)]
		from_email = 'mitnik@catespotr.com'
		order_information = {
			'transaction':transaction,
			'order_items':order_items
		}
		message = get_template('email/order_email.html').render(order_information)
		msg = EmailMessage(subject, message, to=to, from_email=from_email)
		msg.content_type = 'html'
		msg.send()
	except IOError as e:
		return e
