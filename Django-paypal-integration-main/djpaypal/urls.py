from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PaymentApp.urls')),
    path('', include('ProductsApp.urls')),
    path('', include('paypal.standard.ipn.urls')),
]
