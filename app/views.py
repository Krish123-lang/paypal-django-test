from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from app.models import Products
from django.urls import reverse_lazy, reverse
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid


class ProductList(ListView):
    model = Products
    template_name = "app/list.html"
    context_object_name = "list"


class ProductDetail(DetailView):
    model = Products
    template_name = "app/detail.html"

    def get(self, request, pk):
        product = Products.objects.get(id=pk)
        host = request.get_host()
        paypal_checkout = {
            'business': settings.PAYPAL_RECEIVER_EMAIL,
            'amount': product.price,
            'item_name': product.title,
            'invoice': uuid.uuid4(),
            'currency_code': 'USD',
            'notify_url': f"http://{host}{reverse('paypal-ipn')}",
            'return_url': f"http://{host}{reverse('payment-success', kwargs={'pk': pk})}",
            'cancel_url': f"http://{host}{reverse('payment-failed', kwargs={'pk': pk})}",
        }
        paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
        context = {
            'product': product,
            'paypal': paypal_payment
        }
        return render(request, self.template_name, context)


class ProductCreate(CreateView):
    model = Products
    fields = ["title", "content", "image", "price"]
    template_name = "app/create.html"
    success_url = reverse_lazy('list')


class ProductUpdate(UpdateView):
    model = Products
    fields = ["title", "content", "image", "price"]
    template_name = "app/update.html"
    success_url = reverse_lazy('list')


class ProductDelete(DeleteView):
    model = Products
    template_name = "app/delete.html"
    context_object_name = "delete"
    success_url = reverse_lazy("list")
