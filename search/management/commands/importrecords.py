#!/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
import json
import scorched

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Import jsonlines file into Solr collection.'

    def add_arguments(self, parser):
        parser.add_argument('file', type=argparse.FileType('r'), help='Jsonlines file')

    def handle(self, *args, **options):
        solr = scorched.SolrInterface(settings.SOLR_URLS['credentials'])

        with options['file'] as jl_file:
            count = 0
            for row in jl_file:
                try:
                    document = json.loads(row)
                    doc_id = '{}:{}:{}'.format(
                        document['username'],
                        document['domain'],
                        document['password'])
                    document['id'] = doc_id
                    solr.add(document)
                    count += 1
                except Exception as e:
                    self.stdout.write(
                        self.style.WARNING(
                            '{} was not added: {}'.format(row, e)))

            try:
                solr.commit()
            except Exception as e:
                raise CommandError(
                    'Documents could not be added: {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Successfully added {} documents'.format(count)))
