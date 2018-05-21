#!/usr/bin/env python
# -*- coding: utf-8 -*-
# from django.conf import settings
from django.core.management.base import BaseCommand

from payments.monero import update_monero_payments


class Command(BaseCommand):
    help = 'Update Monero payments for all accounts.'

    def handle(self, *args, **options):
        update_monero_payments()

        self.stdout.write(
            self.style.SUCCESS(
                'Updated monero payments.'))
