# Django Paypal Test

1. > django-admin startproject djpaypal .
2. > python manage.py startapp PaymentApp
3. > python manage.py startapp ProductsApp
4. > Create `templates` in `BASE_DIR`
5. > templates  -> `checkout.html` -> `payment-failed.html` -> `payment-success.html` -> `product.html`
6. ## settings.py
```
INSTALLED_APPS = [
    ...    
    'PaymentApp',
    'ProductsApp',
    'paypal.standard.ipn',
]

PAYPAL_RECEIVER_EMAIL = 'apple.business@gmail.com' # where cash is paid into
PAYPAL_TEST = True

# \PAYPAL_BUY_BUTTON_IMAGE = 'https://res.cloudinary.com/the-proton-guy/image/upload/v1685882223/paypal-PhotoRoom_v9pay7.png'
```
7. > urls.py(project)
```
from django.urls import path, include

urlpatterns = [
    path('', include('PaymentApp.urls')),
    path('', include('ProductsApp.urls')),
    path('', include('paypal.standard.ipn.urls')),
]
```
## PaymentApp
1. urls.py(paymentApp)
```
from django.urls import path
from . import views

urlpatterns = [
    path('checkout/<int:product_id>/', views.CheckOut, name='checkout'),
    path('payment-success/<int:product_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:product_id>/', views.paymentFailed, name='payment-failed'),
]
```
2. > views.py
```
from django.shortcuts import render
from ProductsApp.models import Product
from paypal.standard.forms import PayPalPaymentsForm
from django.conf import settings
import uuid
from django.urls import reverse

def CheckOut(request, product_id):
    product = Product.objects.get(id=product_id)
    host = request.get_host()
    paypal_checkout = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': product.price,
        'item_name': product.name,
        'invoice': uuid.uuid4(),
        'currency_code': 'USD',
        'notify_url': f"http: //{host}{reverse('paypal-ipn')}",
        'return_url': f"http: //{host}{reverse('payment-success', kwargs={'product_id': product.id})}",
        'cancel_url': f"http: //{host}{reverse('payment-failed', kwargs={'product_id': product.id})}",
    }
    paypal_payment = PayPalPaymentsForm(initial=paypal_checkout)
    context = {
        'product': product,
        'paypal': paypal_payment
    }
    return render(request, 'checkout.html', context)


def PaymentSuccessful(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'payment-success.html', {'product': product})


def paymentFailed(request, product_id):
    product = Product.objects.get(id=product_id)
    return render(request, 'payment-failed.html', {'product': product})
```
## ProductsApp
1. > models.py(productsApp)
```
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=225)
    description = models.TextField()
    price = models.IntegerField()
    image = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
```
2. > urls.py(productApp)
```
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductView, name='products'),
]
```
3. > views.py(productsApp)
```
from django.shortcuts import render
from .models import Product

def ProductView(request):
    get_products = Product.objects.all()
    return render(request, 'product.html', {'products': get_products})
```
## Templates (BASE_DIR)
1. > checkout.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout page</title>
</head>
<body>
    <h1>Checkout for product: {{product.name}}</h1>
    <div class="product-container">
        <div class="products">
            <img class="img" src="{{product.image}}" alt="">
            <p>{{product.name}}</p>
            <p>Price: $ {{product.price}}</p>
            <p>Description: {{product.description}}</p>
            <!-- <button>Purchase</button> -->
            {{paypal.render}}
        </div>  
    </div>
    <style>
        body {
            padding: 10px;
            box-sizing: border-box;
        }

        .product-container {
            display: flex;
            flex-direction: row;
            width: 100%;
            height: 100vh;
        }
        .img {
            width: 60%;
            border-radius: 50px;
        }
        button {
            padding: 10px;
            border-radius: 5px;
            background-color: dodgerblue;
            color: white;
            border: none;
        }
    </style>
</body>
</html>
```
2. > payment-failed.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment failed</title>
</head>
<body>
    <h1>Payment failed for product: {{product.name}}</h1>
    <div class="product-container">
        <div class="products">
            <img class="img" src="{{product.image}}" alt="">
            <p>{{product.name}}</p>
            <p>Price: $ {{product.price}}</p>
            <p>Description: {{product.description}}</p>

        </div>  
    </div>
    <style>
        body {
            padding: 10px;
            box-sizing: border-box;
        }

        .product-container {
            display: flex;
            flex-direction: row;
            width: 100%;
            height: 100vh;
        }
        .img {
            width: 60%;
            border-radius: 50px;
        }
        button {
            padding: 10px;
            border-radius: 5px;
            background-color: dodgerblue;
            color: white;
            border: none;
        }
    </style>
</body>
</html>
```
3. > payment-success.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment successful</title>
</head>
<body>
    <h1>Payment successful for product: {{product.name}}</h1>
    <div class="product-container">
        <div class="products">
            <img class="img" src="{{product.image}}" alt="">
            <p>{{product.name}}</p>
            <p>Price: $ {{product.price}}</p>
            <p>Description: {{product.description}}</p>

        </div>  
    </div>
    <style>
        body {
            padding: 10px;
            box-sizing: border-box;
        }

        .product-container {
            display: flex;
            flex-direction: row;
            width: 100%;
            height: 100vh;
        }
        .img {
            width: 60%;
            border-radius: 50px;
        }
        button {
            padding: 10px;
            border-radius: 5px;
            background-color: dodgerblue;
            color: white;
            border: none;
        }
    </style>
</body>
</html>
```
4. > product.html
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Products page</title>
</head>
<body>
    <h1>Products</h1>
    <div class="product-container">
        {% for i in products %}
            <div class="products">
                <a href="{% url 'checkout' i.id %}">
                    <img class="img" src="{{i.image}}" alt="">
                </a><br>
                <a href="{% url 'checkout' i.id %}">{{i.name}}</a>
                <p>$ {{i.price}}</p>
            </div>
        {% endfor %}
    </div>
    <style>
        body {
            padding: 10px;
            box-sizing: border-box;
        }

        .product-container {
            display: flex;
            flex-direction: row;
            width: 100%;
            height: 100vh;
        }
        .img {
            width: 60%;
            border-radius: 50px;
        }
    </style>
</body>
</html>
```
# FINISH