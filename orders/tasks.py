from celery import task
from .models import Order
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

import stripe
stripe.api_key = settings.STRIPE_SK


@task
def sent_email(order_id, payment_failed=False):
    order = Order.objects.get(id=order_id)

    message = render_to_string('orders/emailTemplate.html', {'order': order})

    print(settings.EMAIL_HOST_USER)
    print(settings.EMAIL_HOST_PASSWORD)

    if payment_failed:
        mail_sent = send_mail(
            'Payment unsuccessful from Pinnochio"s Pizza & Subs',
            '''
            Sorry, your order cannot be confirmed as payment was unsuccessful. 
            Please try again later.
            ''',
            settings.EMAIL_HOST_USER,
            [order.owner.email],
            fail_silently=False,
        )
    else:
        mail_sent = send_mail(
            "Thanks for ordering from Pinnochio's Pizza & Subs",
            message,
            settings.EMAIL_HOST_USER,
            [order.owner.email],
            fail_silently=False,
        )

    order.paid = True
    order.mark_order_items()
    order.save()

    return mail_sent


@task
def make_payment(order_id, stripe_token):
    order = Order.objects.get(id=order_id)
    try:
        # Use Stripe's library to make requests...
        amount = int(float(order.tot_quant_n_cost()[1]) * 100)

        customer = stripe.Customer.create(
            email=order.owner.email,
            name=order.owner.username,
            shipping={
                'name': order.owner.username,
                'address': {
                    'line1': order.address,
                    'postal_code': order.postal_code,
                    'city': order.city,
                    'state': order.state,
                    'country': order.country,
                }
            },
            source=stripe_token
        )

        charge = stripe.Charge.create(
            customer=customer,
            amount=amount,
            currency="usd",
            description="Pizza order"
        )

        # if above payment process was successful then send order confirmation mail
        sent_email.delay(order.id)

    except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught
        sent_email.delay(order.id, payment_failed=True)
        # print('Status is: %s' % e.http_status)
        # print('Type is: %s' % e.error.type)
        # print('Code is: %s' % e.error.code)
        # # param is '' in this case
        # print('Param is: %s' % e.error.param)
        # print('Message is: %s' % e.error.message)

    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        sent_email.delay(order.id, payment_failed=True)

    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
        sent_email.delay(order.id, payment_failed=True)

    except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
        sent_email.delay(order.id, payment_failed=True)

    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        sent_email.delay(order.id, payment_failed=True)

    except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
        sent_email.delay(order.id, payment_failed=True)

    except Exception as e:
        # Something else happened, completely unrelated to Stripe
        sent_email.delay(order.id, payment_failed=True)
