#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from account.models import Account


class Command(BaseCommand):
    help = 'Create user account.'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID')

    def handle(self, *args, **options):
        try:
            user = User.objects.get(id=options['user_id'])
        except User.DoesNotExist:
            raise CommandError(
                'User ID {} not found.'.format(options['user_id']))

        account = Account(user=user)
        try:
            account.save()
        except Exception as e:
            raise CommandError(
                'Could not create account: {}'.format(e))

        self.stdout.write(
            self.style.SUCCESS(
                'Created account for user ID {}'.format(options['user_id'])))
