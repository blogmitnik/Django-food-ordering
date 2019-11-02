from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('edit_profile/', views.editProfileView, name='edit_profile'),
    path('change_password/', views.change_password, name='change_password'),
]