from django.urls import path
from . import views

app_name = 'like'

urlpatterns = [
    path('product/<slug:product_slug>', views.like_or_unlike_item, name='like_product'),
]