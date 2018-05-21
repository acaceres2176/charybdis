from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render
from django.utils import timezone
from django.views import View


from .models import Account


class AccountView(LoginRequiredMixin, View):
    template_name = 'account/index.html'

    def get(self, request, *args, **kwargs):
        days = 0
        hours = 0
        minutes = 0
        expired = True
        label = 'danger'
        status = 'Inactive'

        try:
            account = Account.objects.get(user=request.user)
        except Account.DoesNotExist:
            raise Http404('Account does not exist')

        if account.expires > timezone.now():
            expired = False
            label = 'success'

        if not expired:
            diff = account.expires - timezone.now()
            days, seconds = diff.days, diff.seconds
            hours = days * 24 + seconds // 3600
            minutes = (seconds % 3600) // 60
            status = 'Active'

        time_remaining = '{} days, {} hours, {} minutes'.format(
            days, hours, minutes)
        context_data = {'account': account,
                        'label': label,
                        'status': status,
                        'time_remaining': time_remaining}
        return render(request, self.template_name, context_data)
