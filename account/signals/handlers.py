# -*- coding: utf-8 -*-
import logging

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from account.models import Account

logger = logging.getLogger(__name__)


@receiver(post_save, sender=User)
def ensure_account_exists(sender, **kwargs):
    logger.info('Signal for User.post_save received')
    if kwargs.get('created', False):
        user = kwargs.get('instance')
        Account.objects.get_or_create(user=user)
        logger.info('Created account for: {}'.format(user.id))
