import datetime
from django.utils import timezone
from django.db import models
from django.urls import reverse
from django.db.models import Q

class Place(models.Model):
	name = models.CharField(max_length=200)
	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='place', blank=True, default='place-default.jpg')

	def get_url(self):
		return reverse('shop:restaurants', args=[self.slug])

	def __str__(self):
		return self.name

class Category(models.Model):
	IS_SELECTED = (  
	    (0, 'Not Selected'),
	    (1, 'Selected Alreday'),
	)
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='category', blank=True, default='shop-default.jpg')
	place = models.ForeignKey(Place, on_delete=models.CASCADE, default=1)
	select = models.PositiveSmallIntegerField(choices=IS_SELECTED, default=1)

	class Meta:
		ordering = ['-select']
		verbose_name = 'category'
		verbose_name_plural = 'categories'

	def select_status_str(self):
		return str(self.IS_SELECTED[self.select][1])

	def get_url(self):
		return reverse('shop:products_by_category', args=[self.slug])

	def __str__(self):
		return str(self.name) if self.name else ''

class Product(models.Model):
	name = models.CharField(max_length=255, unique=True)
	slug = models.SlugField(max_length=255, unique=True)
	description = models.TextField(blank=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	image = models.ImageField(upload_to='product', blank=True, default='food-default.jpg')
	stock = models.IntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now_add=True)
	star = models.IntegerField(default=0)

	class Meta:
		ordering = ['name']
		verbose_name = 'product'
		verbose_name_plural = 'products'

	def get_url(self):
		return reverse('shop:product_detail', args=[self.category.slug, self.slug])

	def __str__(self):
		return str(self.name) if self.name else ''

	def can_be_order(self, user):
		return self.category.select == 1 and self.category.place == user.userprofile.location.parent and user.userprofile.can_order

	def was_new_arrival(self):
		now = timezone.now()
		return now - datetime.timedelta(days=7) <= self.created <= now

	was_new_arrival.admin_order_field = 'pub_date'
	was_new_arrival.boolean = True
	was_new_arrival.short_description = 'New Arrival?'