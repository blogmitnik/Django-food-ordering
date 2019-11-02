from django.db import models

class Order(models.Model):
	PENDING = 0
	DONE = 1
	ORDER_STATUS = (
		(PENDING, 'Pending'), 
		(DONE, 'Done'),
	)
	ORDER_PLACES = (
		(1, 'QRDC Taipei'), 
		(2, 'CSMC A Factory'), 
		(3, 'CSMC C Factory'), 
		(4, 'CSMC D Factory'),
		(5, 'QSMC F4'),
	)

	total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Order Total")
	emailAddress = models.EmailField(max_length=250, blank=True, verbose_name="Email Address")
	created = models.DateField(auto_now_add=True)
	shippingName = models.CharField(max_length=250, blank=True)
	status = models.PositiveSmallIntegerField(choices=ORDER_STATUS, default=0)
	location = models.PositiveSmallIntegerField(choices=ORDER_PLACES, default=0)

	class Meta:
		db_table = 'Order'
		ordering = ['-created']

	def order_status_str(self):
		return str(self.ORDER_STATUS[self.status][1])

	def order_place_str(self):
		return str(self.ORDER_PLACES[self.location-1][1])

	def __str__(self):
		return str(self.id)

class OrderItem(models.Model):
	product = models.CharField(max_length=250)
	quantity = models.IntegerField()
	price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
	order = models.ForeignKey(Order, on_delete=models.CASCADE)
	memo = models.TextField(max_length=250, blank=True)

	class Meta:
		db_table = 'OrderItem'

	def sub_total(self):
		return self.quantity * self.price

	def __str__(self):
		return self.product