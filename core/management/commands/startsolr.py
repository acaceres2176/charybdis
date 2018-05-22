#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Starts solr daemon.'

    def handle(self, *args, **options):
        solr_dir_path = os.path.join(settings.BASE_DIR, 'solr')
        solr_bin_path = os.path.join(solr_dir_path, 'bin', 'solr')

        try:
            subprocess.check_output([solr_bin_path, 'start'])
        except Exception as e:
            raise CommandError(
                'Could not start solr {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Started solr'))
