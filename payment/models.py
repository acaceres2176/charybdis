from django.utils import timezone
from django.db import models

from account.models import Account


# class MoneroPayment(models.Model):
#     tx_hash = models.CharField(max_length=200, unique=True)
#     acount = models.FloatField()
#     block_height = models.IntegerField()
#     payment_id = models.CharField(max_length=100)
#     unlock_time = models.IntegerField()
#     dollar_value = models.FloatField(default=0)
#     usd_rate = models.FloatField(default=0)
#     account_minutes = models.FloatField(default=0)
#
#
# class MoneroLog(models.Model):
#     completed = models.DateTimeField(default=timezone.now)
#     new_payments = models.IntegerField()
#     payment_ids = models.IntegerField()
#     block_height = models.IntegerField()


class StripePayment(models.Model):
    charge_id = models.CharField(max_length=250)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    created = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=250, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    days = models.IntegerField(default=30)
    expires = models.DateTimeField(default=timezone.now)
