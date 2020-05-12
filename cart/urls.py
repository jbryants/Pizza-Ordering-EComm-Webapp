from django.urls import path
from .views import CartListView, addItem, updateItem

app_name = 'cart'

urlpatterns = [
    path('', CartListView.as_view(), name="details"),
    path('add/', addItem, name='add_item'),
    path('update/', updateItem, name="update_item"),
]