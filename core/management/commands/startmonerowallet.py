#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts monero wallet.'

    def add_arguments(self, parser):
        parser.add_argument('password', type=str)

    def handle(self, *args, **options):
        try:
            subprocess.check_call(
                [
                    'monero-wallet-cli',
                    '--wallet-file', settings.MONERO_WALLET_FILE,
                    '--password', options['password'],
                    '--rpc-bind-ip', settings.MONERO_WALLET_HOST,
                    '--rpc-bind-port', settings.MONERO_WALLET_PORT,
                ])
        except Exception as e:
            raise CommandError(
                'Could not start monerowallet {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Started monero wallet on {}:{}'.format(settings.MONERO_WALLET_HOST,
                                                        settings.MONERO_WALLET_PORT)))
