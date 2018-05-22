import logging
import scorched

from django.apps import AppConfig
from django.conf import settings


logger = logging.getLogger(__name__)


class SearchConfig(AppConfig):
    name = 'search'
    solr_urls = settings.SOLR_URLS
    solr = None

    def get_solr(self):
        return scorched.SolrInterface(self.solr_urls['credentials'])

    def ready(self):
        # ToDo - run some tests
        try:
            self.solr = self.get_solr()
        except Exception as e:
            logger.warning('Could not initialize solr: {}'.format(e))
            logger.warning('If you are running the startsolr command, this warning can be safely ignored')
