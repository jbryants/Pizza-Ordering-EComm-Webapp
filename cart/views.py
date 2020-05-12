from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from orders.models import Order
from cart.cart import Cart

import json
from django.http import JsonResponse


class CartListView(LoginRequiredMixin, ListView):
    login_url = "/auth/login"
    template_name = "cart/viewCart.html"
    context_object_name = "order"
    model = Order

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # select options 1 to 20
        context['options_list'] = [i for i in range(1, 21)]
        return context

    def get_queryset(self):
        # current user's active order which is not completed.
        return Order.objects.filter(owner=self.request.user, paid=False).first()


@login_required(login_url='/auth/login')
def addItem(request):
    data = json.loads(request.body)

    cart = Cart(request)

    cart.add(data)

    response = {"added": True}

    response["totalItems"], response["totalPrice"] = cart.order.tot_quant_n_cost()

    return JsonResponse(response)


@login_required(login_url='/auth/login')
def updateItem(request):
    data = json.loads(request.body)

    cart = Cart(request)

    price = cart.update(data)

    response = {"updated": True, "price": price}

    response["totalItems"], response["totalPrice"] = cart.order.tot_quant_n_cost()

    return JsonResponse(response)

