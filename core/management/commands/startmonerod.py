#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts monero daemon.'

    def handle(self, *args, **options):
        monero_path = os.path.join(settings.BASE_DIR, 'monero')
        monerod_path = os.path.join(monero_path, 'monerod')
        try:
            subprocess.check_call([monerod_path])
        except Exception as e:
            raise CommandError(
                'Could not start monerod {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Started monerod'))
