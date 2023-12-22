from django.shortcuts import render

from app.models import Products

# Create your views here.
from django.views.generic.detail import DetailView


class PaymentSuccessful(DetailView):
    model = Products
    context_object_name = "product"
    template_name = "app/payment-success.html"


class PaymentFailed(DetailView):
    model = Products
    context_object_name = "product"
    template_name = "app/payment-failed.html"


# def PaymentSuccessful(request, pk):
#     product = Products.objects.get(id=pk)
#     return render(request, 'payment-success.html', {'product': product})


# def paymentFailed(request, pk):
#     product = Products.objects.get(id=pk)
#     return render(request, 'payment-failed.html', {'product': product})
