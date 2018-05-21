import stripe

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from django.views import View

from .models import StripePayment
from account.models import Account


class PaymentView(LoginRequiredMixin, View):
    template_name = 'payment/index.html'

    def get(self, request, *args, **kwargs):
        context_data = {}
        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        try:
            token = request.POST['stripeToken']
        except KeyError:
            return HttpResponse('Invalid request', status=400)

        try:
            account = Account.objects.get(user=request.user)
        except:
            return HttpResponse('Account not found', status=404)

        try:
            charge = stripe.Charge.create(
                amount=999,
                currency='usd',
                description='Example charge',
                source=token,
            )
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught
            body = e.json_body
            err = body.get('error', {})
            return HttpResponse(err.get('message'), status='400')
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            return HttpResponse(
                'There was an issue communicating with the payment processor. '
                ' Please try again',
                status=500)
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        except Exception as e:
            # Something else happened, completely unrelated to Stripe
            return HttpResponse(
                'Invalid request to Stripe. Please contact support',
                status=500)
        # Save a record of the payment
        payment = StripePayment(
            charge_id=charge.id,
            amount=charge.amount,
            created=timezone.datetime.fromtimestamp(charge.created),
            account=account,
            email=charge.receipt_email)
        payment.save()
        payments = StripePayment.objects.filter(account=account)

        context_data = {'payments': payments}
        return render(request, self.template_name, context_data)
