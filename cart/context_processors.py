from orders.models import Order
from .cart import Cart


def cart(request):
    return {'cart': Cart(request)}
