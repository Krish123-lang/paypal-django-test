from django.urls import path
from . import views

urlpatterns = [
    path('payment-success/<pk>/', views.PaymentSuccessful.as_view(), name='payment-success'),
    path('payment-failed/<pk>/', views.PaymentFailed.as_view(), name='payment-failed'),
]
