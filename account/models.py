from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AccountException(Exception):
    pass


# def generate_monero_payment_id():
#     """
#     Return random monero payment_id.
#
#     Generate some random payment_id for the
#     monero transactions.
#
#     payment_id is 32 bytes (64 hexadecimal characters)
#     thus we first generate 32 random byte array
#     which is then change to string representation, since
#     json will not not what to do with the byte array.
#
#     https://moneroexamples.github.io/python-json-rpc/
#     """
#     random_32_bytes = os.urandom(32)
#     payment_id = "".join(map(chr, binascii.hexlify(random_32_bytes)))
#
#     return payment_id


# class Account(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     monero_payment_id = models.CharField(max_length=100,
#                                          default=generate_monero_payment_id)
#     monero_wallet_address = models.CharField(max_length=200,
#                                              null=True,
#                                              blank=True)
#     expires = models.DateTimeField(default=timezone.now)
#
#     def save(self, *args, **kwargs):
#         """
#         Override save method in order to ensure account has
#         integrated monero wallet address.
#         """
#         if not self.monero_wallet_address:
#             mw = apps.get_app_config('account').mw
#             response = mw.make_integrated_address(self.monero_payment_id)
#
#             try:
#                 self.monero_wallet_address = response['integrated_address']
#             except Exception as e:
#                 raise AccountException(
#                     'Could not create monero address: {}'.format(e))
#
#         super().save(*args, **kwargs)  # Call the "real" save() method.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expires = models.DateTimeField(default=timezone.now)
