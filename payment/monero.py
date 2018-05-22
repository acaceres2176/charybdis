#!/usr/bin/env python
# -*- coding: utf-8 -*-
import ccxt
from datetime import datetime
from django.apps import apps
from django.conf import settings
from django.utils import timezone

from account.models import Account
from payment.models import MoneroPayment, MoneroLog


class MoneroException(Exception):
    raise


def minutes_paid_for(monero_amount, monero_usd_rate):
    """
    Return minutes paid-for by monero_amount.

    :param monero_amount: float monero amount.
    :param monero_usd_rate: monero to usd exchange rate.
    :returns: float number of minutes.
    """
    dollar_amount = monero_amount * monero_usd_rate
    account_minutes = dollar_amount * settings.DOLLARS_PER_MINUTE

    return account_minutes


def update_monero_payments():
    accounts = Account.objects.all()
    payment_accounts = dict()
    payment_ids = set()
    for account in accounts:
        payment_accounts[account.payment_id] = account
        payment_ids.add(account.payment_id)
    # Get payments for all payment IDs..
    if payment_ids:
        try:
            monero_data = ccxt.bitfinex().fetch_ticker('XMR/USD')
            monero_usd_rate = monero_data['last']
        except Exception as e:
            raise MoneroException(
                'Could not get Monero data from bitfinex: {}'.format(e))

        last_block_height = MoneroLog.objects.max('block_height')
        mw = apps.get_app_config('account').mw
        payments = mw.get_bulk_payments(payment_ids, last_block_height)
        new_payment_ids = ()

        for payment in payments:
            dollar_amount = payment['amount'] * monero_usd_rate
            minutes = dollar_amount * settings.DOLLARS_PER_MINUTE
            monero_payment = MoneroPayment(
                tx_hash=payment['tx_hash'],
                amount=payment['amount'],
                block_height=payment['block_height'],
                payment_id=payment['payment_id'],
                unlock_time=payment['unlock_time'],
                account_minutes=minutes,
                usd_rate=monero_usd_rate,
                dollar_value=dollar_amount
            )

            # Update block height
            if payment['block_height'] > last_block_height:
                last_block_height = payment['block_height']

            new_payment_ids.add(payment['payment_id'])
            monero_payment.save()

            # Update the account
            account = payment_accounts[payment['payment_id']]
            minutes = minutes_paid_for(payment['amount'])

            if account.expires < timezone.now():
                account.expires = timezone.now() + datetime.timedelta(
                    minutes=minutes)
            else:
                account.expires = account.expires + datetime.timedelta(
                    minutes=minutes)

            account.save()

            # Log the update
            log = MoneroLog(new_payments=len(payments),
                            payment_ids=len(new_payment_ids),
                            block_height=last_block_height)

            log.save()
