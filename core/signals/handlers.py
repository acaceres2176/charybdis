# -*- coding: utf-8 -*-
from django.contrib.auth.signals import user_logged_in
from django.contrib import messages
from django.dispatch import receiver


@receiver(user_logged_in)
def login_handler(sender, user, request, **kwargs):
    """
    Add a welcome message when the user logs in
    """
    messages.info(request, "Welcome, {}!".format(user))
