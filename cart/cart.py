from django.conf import settings
from menu.models import Product
from orders.models import OrderItem, Order
from decimal import Decimal
import json


def get_add_ons(add_ons_str):
    """
    Clean data and return toppings or extras add ons
    """
    # remove duplicates from toppings if any
    add_ons_ids = set(add_ons_str.split(' '))
    # remove empty "" if any
    add_ons_ids = [id for id in add_ons_ids if id != '']

    add_ons = []
    for id in add_ons_ids:
        add_ons.append(Product.objects.get(id=id))

    return add_ons


class Cart(object):

    def __init__(self, request):
        """
        Initialize the cart.
        """
        self.session = request.session
        self.user = request.user
        if request.user.is_authenticated:
            self.order, status = Order.objects.get_or_create(owner=request.user, paid=False)

        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}

    def add(self, data):
        """
        add a new item to cart or update existing quantity
        """
        product = Product.objects.get(id=data["productId"])

        toppings = get_add_ons(data['toppings'])
        extras = get_add_ons(data['extras'])

        order_item, stat = OrderItem.objects.get_or_create(owner=self.user,
                                                        product=product,
                                                        price=(product.price + Decimal(0.50 * len(extras))),
                                                        topping1=toppings[0] if 0 < len(toppings) else None,
                                                        topping2=toppings[1] if 1 < len(toppings) else None,
                                                        topping3=toppings[2] if 2 < len(toppings) else None,
                                                        extras1=extras[0] if 0 < len(extras) else None,
                                                        extras2=extras[1] if 1 < len(extras) else None,
                                                        extras3=extras[2] if 2 < len(extras) else None,
                                                        extras4=extras[3] if 3 < len(extras) else None,
                                                        ordered=False)

        order_item.quantity += int(data['quantity'])
        order_item.save()

        # order, ordStatus = Order.objects.get_or_create(owner=self.user, paid=False)
        self.order.items.add(order_item)
        self.order.save()

    def update(self, data):
        """
        update quantity of item in cart
        and return updated cost
        """
        order_item = OrderItem.objects.get(id=data['itemId'])
        order_item.quantity = Decimal(data['quantity'])
        order_item.save()

        return order_item.get_cost()

    def clear(self):
        """
        remove cart from session
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
