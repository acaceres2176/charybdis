#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pprint as pp
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'List users.'

    def handle(self, *args, **options):
        users = User.objects.all()
        for user in users:
            pp.pprint(user.__dict__)
