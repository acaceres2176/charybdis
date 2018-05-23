import logging
import stripe

from datetime import timedelta
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from .models import StripePayment
from account.models import Account


class PaymentView(LoginRequiredMixin, View):
    template_name = 'payment/index.html'
    logger = logging.getLogger('PaymentView')

    def __init__(self, *args, **kwargs):
        super().__init__()
        if settings.STRIPE_LIVE_MODE:
            self.stripe_public_key = settings.STRIPE_LIVE_PUBLIC_KEY
            stripe.api_key = settings.STRIPE_LIVE_SECRET_KEY
        else:
            self.stripe_public_key = settings.STRIPE_TEST_PUBLIC_KEY
            stripe.api_key = settings.STRIPE_TEST_SECRET_KEY

    def get(self, request, *args, **kwargs):
        account = Account.objects.get(user=request.user)
        amount = 29
        cent_amount = amount * 100
        payments = StripePayment.objects.filter(account=account).order_by('-created')
        context_data = {'payments': payments,
                        'amount': amount,
                        'cent_amount': cent_amount,
                        'stripe_public_key': self.stripe_public_key}
        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        if 'amount-selected' in request.POST:
            amount = int(request.POST['amount-selected'])
            account = Account.objects.get(user=request.user)
            payments = StripePayment.objects.filter(account=account).order_by('-created')
            context_data = {'payments': payments,
                            'amount': amount,
                            'cent_amount': amount * 100,
                            'stripe_public_key': self.stripe_public_key}
            return render(request, self.template_name, context_data)

        try:
            token = request.POST['stripeToken']
        except KeyError:
            return HttpResponse('Bad request: missing Stripe token.', status=400)

        try:
            account = Account.objects.get(user=request.user)
        except:
            return HttpResponse('Account not found', status=404)

        try:
            email = request.POST['stripeEmail']
        except KeyError:
            return HttpResponse('Bad request: invalid email.', status=400)

        try:
            amount = int(request.POST['amount']) * 100  # cents
        except KeyError:
            return HttpResponse('Bad request: missing payment amount.', status=400)

        try:
            days = settings.PAYMENT_DAYS[amount]
        except KeyError:
            return HttpResponse('Bad request: invalid payment amount: {}'.format(amount), status=400)

        try:
            charge = stripe.Charge.create(
                amount=amount,
                currency='usd',
                description='{} day(s)'.format(days),
                source=token,
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            return HttpResponse(err.get('message'), status='400')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            self.logger.critical(e)
            return HttpResponse(
                'There was an issue communicating with the payment processor. '
                ' Please try again',
                status=500)
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            self.logger.critical(e)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            self.logger.critical(e)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            self.logger.critical(e)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            self.logger.critical(e)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            self.logger.critical(e)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)

        # Update account with new expiry time
        if account.expires < timezone.now():
            expires = timezone.now() + timedelta(days=days)
        else:
            expires = account.expires + timedelta(days=days)
        account.expires = expires
        account.save()

        # Save payment
        amount = charge.amount / 100
        cent_amount = charge.amount
        payment = StripePayment(
            charge_id=charge.id,
            amount=amount,
            created=timezone.datetime.fromtimestamp(charge.created),
            account=account,
            days=days,
            expires=expires,
            email=email)
        payment.save()
        payments = StripePayment.objects.filter(account=account).order_by('-created')

        messages.success(request, 'Payment successful!')
        context_data = {'payments': payments,
                        'amount': amount,
                        'cent_amount': cent_amount,
                        'stripe_public_key': self.stripe_public_key}
        return render(request, self.template_name, context_data)
