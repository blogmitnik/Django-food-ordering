"""django_hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path, reverse_lazy
from django.conf.urls import url
from django.contrib.auth import views as auth_views
from shop import views as shopviews

urlpatterns = [
    url(r'^$', shopviews.HomeView.as_view(), name='home'),
    url(r'^accounts/register/', shopviews.signupView, name='signup'),
    url(r'^accounts/login/', shopviews.signinView, name='signin'),
    url(r'^signout/', shopviews.signoutView, name='signout'),
    url(r'^shop/', include('shop.urls')),
    url(r'^cart/', include('cart.urls')),
    url(r'^search/', include('search_app.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^like/', include('like.urls')),
    url(r'^user/', include('user.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='admin/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page=reverse_lazy('home')), name='logout'),
    url(r'^place', shopviews.SelectPlace, name='choice_place'),
    url(r"^ratings/", include("ratings.urls", namespace="pinax_ratings")),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)