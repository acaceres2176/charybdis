#!/usr/bin/env python
# -*- coding: utf-8 -*-
import scorched

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Deletes all credential data from Solr collection.'

    def handle(self, *args, **options):
        solr = scorched.SolrInterface(settings.SOLR_URLS['credentials'])

        try:
            solr.delete_all()
            solr.commit()
        except Exception as e:
            raise CommandError(
                'Collection could not be deleted: {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully deleted all records in "credentials" collection'))
