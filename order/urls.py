from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('thanks/<int:order_id>/', views.thanks, name='thanks'),
    path('my_orders/', views.orderHistory, name='history'),
    path('view_detail/<int:order_id>', views.viewOrder, name='order_detail'),
    path('delete_order/<int:order_id>', views.deleteOrder, name='order_delete'),
    path('manage_orders/', views.manageOrders, name='manage_orders'),
    path('<int:order_id>/status/<int:status_id>', views.changeStatus, name='change_status'),
]