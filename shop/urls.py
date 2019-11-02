from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.allProdCat, name='allProdCat'),
    path('sorted/<str:sort_by>/', views.allProdCat, name='allProdCatSorted'),
    path('filter/<str:filter_by>/', views.allProdCat, name='allProdCatFilter'),
    path('filter/<str:filter_by>/sorted/<str:sort_by>/', views.allProdCat, name='allProdCatFilterSorted'),
    path('<slug:c_slug>/', views.allProdCat, name='products_by_category'),
    path('<slug:c_slug>/sorted/<str:sort_by>/', views.allProdCat, name='products_by_category_sorted'),
    path('<slug:c_slug>/filter/<str:filter_by>/', views.allProdCat, name='products_by_category_filter'),
    path('<slug:c_slug>/filter/<str:filter_by>/sorted/<str:sort_by>/', views.allProdCat, name='products_by_category_filter_sorted'),
    path('<slug:c_slug>/<slug:product_slug>', views.ProdCatDetail, name='product_detail'),
    path('<slug:place_slug>/restaurants/', views.shopRestaurants, name='restaurants'),
    path('<int:place_id>/choose_restaurant/', views.selectDefault, name='default_restaurant'),
]