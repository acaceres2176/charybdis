#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Start uwsgi daemon'

    def handle(self, *args, **options):
        ini_path = os.path.join(settings.BASE_DIR, 'uwsgi.ini')

        try:
            subprocess.check_call(['uwsgi', '--ini', ini_path])
        except Exception as e:
            raise CommandError(
                'Could not start uswgi {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Started uwsgi'))
