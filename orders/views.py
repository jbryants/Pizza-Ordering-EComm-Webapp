from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.admin.views.decorators import staff_member_required

from .models import Order
from .forms import OrderForm

import json
from .tasks import make_payment


def cart_check(user):
    """
    only allow to proceed for checkout if cart is not empty
    """
    try:
        if Order.objects.get(owner=user, paid=False).tot_quant_n_cost()[1] > 0:
            return True
        else:
            return False
    except Order.DoesNotExist:
        return False


@login_required(login_url='/auth/login')
@user_passes_test(cart_check, login_url="/cart")
def checkout(request):
    form = OrderForm()

    # if address is already filled, then no need to fill it again.
    if Order.objects.filter(owner=request.user).first().address != "":
        is_done = True
    else:
        is_done = False

    return render(request, "orders/checkout.html", {"form": form, 'isDone': is_done})


@login_required(login_url='/auth/login')
@user_passes_test(cart_check, login_url="/")
def process_form(request):
    instance = get_object_or_404(Order, owner=request.user, paid=False)

    data = json.loads(request.body)

    form = OrderForm(data or None, instance=instance)

    if form.is_valid():
        form.save()
        return JsonResponse({"status": True})
    else:
        errors = {}
        for field in form:
            for error in field.errors:
                error.append(error)

        return JsonResponse({"status": False, 'errors': errors})


@login_required(login_url='/auth/login')
@user_passes_test(cart_check, login_url="/")
def charge(request):
    if request.method == "POST":
        order = Order.objects.get(owner=request.user, paid=False)

        # launch asynchronous task
        make_payment.delay(order.id, request.POST['stripeToken'])

    return redirect('orders:done')


@login_required(login_url='/auth/login')
@user_passes_test(cart_check, login_url="/")
def done(request):
    order = Order.objects.get(owner=request.user, paid=False)
    return render(request, "orders/checkoutCompleted.html", {"order_id": order.id})


@staff_member_required
def orders_list(request):
    orders = Order.objects.filter(paid=True)
    return render(request, "orders/orders_list.html", {"orders": orders})
