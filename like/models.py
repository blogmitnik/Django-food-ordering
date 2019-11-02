from django.db import models
from shop.models import Product
from django.contrib.auth.models import User

class Like(models.Model):
	product = models.ForeignKey(Product, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date_added = models.DateField(auto_now_add=True)
	class Meta:
		db_table = 'Like'
		ordering = ['date_added']

	def __str__(self):
		return self.id