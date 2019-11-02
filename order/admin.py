from django.contrib import admin
from .models import Order, OrderItem

class OrderItemAdmin(admin.TabularInline):
	model = OrderItem
	fieldsets = [
		('Product', {'fields':['product'],}),
		('Quantity', {'fields':['quantity'],}),
		('Price', {'fields':['price'],}),
		('Note', {'fields':['memo'],}),
	]
	readonly_fields = []
	can_delete = True
	ax_num = 0
	template = 'admin/order/tabular.html'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	list_display = ['id', 'total', 'status', 'shippingName', 'location', 'created']
	list_display_links = ('id', 'shippingName')
	list_filter = ['created', 'status', 'shippingName']
	search_fields = ['emailAddress']
	readonly_fields = ['id', 'shippingName', 'emailAddress', 'created']
	fieldsets = [
		('Order Information', {'fields':['id', 'created', 'total', 'status'],}),
		('Billing Information', {'fields':['emailAddress'],}),
		('Shipping Information', {'fields':['shippingName', 'location'],}),
	]

	inlines = [
		OrderItemAdmin,
	]

	def has_delete_permission(self, request, obj=None):
		return True

	def has_add_permission(self, request):
		return True