import logging
from django.apps import AppConfig
from django.conf import settings


logger = logging.getLogger(__name__)


class AccountConfig(AppConfig):
    name = 'account'

    def ready(self):
        import account.signals.handlers  # noqa
        # try:
        #     self.mw = monerowallet.MoneroWallet(
        #         protocol=settings.MONERO_WALLET_PROTOCOL,
        #         host=settings.MONERO_WALLET_HOST,
        #         port=settings.MONERO_WALLET_PORT,
        #         path=settings.MONERO_WALLET_RPC_PATH)
        # except Exception as e:
        #     raise('Could not initialize monerowallet: {}'.format(e))
