from django.conf import settings
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect


def home(request):
    """
    Home page view.
    """
    context_data = {'records': 10000000}

    return render(request, 'core/home.html', context_data)


def contact(request):
    """
    Contact page view.
    """
    return render(request, 'core/contact.html')


def pricing(request):
    """
    Pricing page view.
    """
    context_data = {
        'dollars_per_day': settings.DOLLARS_PER_DAY,
        'dollars_per_month': settings.DOLLARS_PER_MONTH,
        'dollars_per_year': settings.DOLLARS_PER_YEAR,
    }
    return render(request, 'core/pricing.html', context_data)


# def pricing(request):
#     """
#     Pricing page view.
#     """
#     try:
#         monero_data = ccxt.bitfinex().fetch_ticker('XMR/USD')
#         monero_usd_rate = monero_data['last']
#     except:
#         return HttpResponse(status=500)
#
#     dollars_per_hour = round(settings.DOLLARS_PER_SECOND * 60 * 60, 2)
#     dollars_per_day = round(settings.DOLLARS_PER_SECOND * 60 * 60 * 24, 2)
#     dollars_per_month = round(settings.DOLLARS_PER_SECOND * 60 * 60 * 24 * 30, 2)
#     monero_per_hour = dollars_per_hour / monero_usd_rate
#     monero_per_day = dollars_per_day / monero_usd_rate
#     monero_per_month = dollars_per_month / monero_usd_rate
#
#     context_data = {
#         'dollars_per_hour': dollars_per_hour,
#         'dollars_per_day': dollars_per_day,
#         'dollars_per_month': dollars_per_month,
#         'monero_per_hour': monero_per_hour,
#         'monero_per_day': monero_per_day,
#         'monero_per_month': monero_per_month,
#         'monero_usd_rate': monero_usd_rate,
#         'timestamp': timezone.now()
#     }
#
#     return render(request, 'core/pricing.html', context_data)


def signup(request):
    """
    Signup view.
    """
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'core/signup.html', {'form': form})
