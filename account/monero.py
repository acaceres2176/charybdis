#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .models import Account, Payment, PaymentLog


def get_monero_payments():
    accounts = Account.objects.all()
    payment_ids = [a.payment_id for a in accounts]


