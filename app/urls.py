from django.urls import path
from . import views

urlpatterns = [
    path("", views.ProductList.as_view(), name="list"),
    path("create", views.ProductCreate.as_view(), name="create"),
    path("detail/<pk>", views.ProductDetail.as_view(), name="detail"),
    path("update/<pk>", views.ProductUpdate.as_view(), name="update"),
    path("delete/<pk>", views.ProductDelete.as_view(), name="delete"),
]
