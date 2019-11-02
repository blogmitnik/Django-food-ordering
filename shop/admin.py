from django.contrib import admin
from .models import Category, Product, Place

class CategoryInline(admin.StackedInline):
	model = Category
	extra = 3

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'description']
	inlines = [CategoryInline]

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug']
	prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ['name', 'price', 'stock', 'available', 'star', 'created', 'updated', 'was_new_arrival']
	list_editable = ['price', 'stock', 'available']
	prepopulated_fields = {'slug':('name',)}
	list_per_page = 20