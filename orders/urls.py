from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path("", views.checkout, name="checkout"),
    path("processForm/", views.process_form, name="process_form"),
    path("charge/", views.charge, name="charge"),
    path("completed/", views.success, name="success"),
    path("list/", views.orders_list, name="order_list"),
]