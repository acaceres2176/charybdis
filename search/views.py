# import math
import logging

logger = logging.getLogger(__name__)

from cerberus import Validator
from collections import OrderedDict
from django.apps import apps
from django.contrib import messages
from django.shortcuts import render
from django.utils import timezone
from django.views import View
from scorched.strings import RawString, WildcardString
from urllib.parse import (
    urlencode, unquote, urlparse, parse_qsl, ParseResult)


from account.models import Account


def get_args(url):
    """
    Return dictionary of url arguments.

    :param url: URL string
    :returns: dict
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    args = parsed_url.query
    # Converting URL arguments to dict
    parsed_args = dict(parse_qsl(args))
    return parsed_args


def get_ordered_args(args):
    """
    Return an ordered dictionary of URL parameters.
    Keeps URLs consistent.

    :param args: arg dictionary
    returns: OrderedDict
    """
    ordered_args = OrderedDict(
        [
            ('query', args.get('query', '')),
            ('start', args.get('start', 0)),
            ('rows', args.get('rows', 10)),
            ('wildcards', args.get('wildcards', 0)),

        ]
    )
    return ordered_args


def get_ordered_url(url):
    """
    Return a URL with ordered args.

    :param url: URL string
    :returns: string URL
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    args = get_args(url)
    # Order the args
    ordered_args = get_ordered_args(args)
    # Converting URL argument to proper query string
    encoded_args = urlencode(ordered_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_args, parsed_url.fragment
    ).geturl()

    return new_url


def add_url_params(url, params):
    """
    Add GET params to provided URL being aware of existing.

    :param url: string of target URL
    :param params: dict containing requested params to be added
    :return: string with updated URL

    >> url = 'http://stackoverflow.com/test?answers=true'
    >> new_params = {'answers': False, 'data': ['some','values']}
    >> add_url_params(url, new_params)
    'http://stackoverflow.com/test?data=some&data=values&answers=false'
    """
    # Unquoting URL first so we don't loose existing args
    url = unquote(url)
    # Extracting url info
    parsed_url = urlparse(url)
    # Extracting URL arguments from parsed URL
    get_args = parsed_url.query
    # Converting URL arguments to dict
    parsed_get_args = dict(parse_qsl(get_args))
    # Merging URL arguments dict with new params
    parsed_get_args.update(params)
    # Order the args
    ordered_args = get_ordered_args(parsed_get_args)
    # Converting URL argument to proper query string
    encoded_get_args = urlencode(ordered_args, doseq=True)
    # Creating new parsed result object based on provided with new
    # URL arguments. Same thing happens inside of urlparse.
    new_url = ParseResult(
        parsed_url.scheme, parsed_url.netloc, parsed_url.path,
        parsed_url.params, encoded_get_args, parsed_url.fragment
    ).geturl()

    return new_url


class SearchView(View):
    solr = apps.get_app_config('search').solr
    template_name = 'search/index.html'
    paginate_by = 10
    schema = {
        'query': {'type': 'string'},
        'wildcards': {'type': 'boolean', 'default': False},
        'start': {'type': 'integer', 'default': 0},
        'rows': {'type': 'integer', 'default': 10},
    }

    def __init__(self):
        self.validator = Validator(self.schema)

    def _parse_options(self, request):
        """
        Parse options from GET request.
        """
        options = dict(request.GET.items())
        # Attempt to convert values to schema types
        for key, scheme in self.schema.items():
            if key in options:
                if scheme['type'] == 'boolean':
                    try:
                        options[key] = bool(int(options[key]))
                    except Exception as e:
                        pass
                if scheme['type'] == 'integer':
                    try:
                        options[key] = int(options[key])
                    except:
                        pass
            else:
                options[key] = None
        return options

    def _validate_options(self, options):
        """
        Validate options against schema using cerberus.
        """
        validator = Validator(self.schema)
        valid = validator.validate(options)
        return valid, validator.errors

    def _solr_query(self, options):
        """
        Return solr response object.
        """
        if options['wildcards'] is True:
            query = WildcardString(options['query'])
        else:
            query = RawString(options['query'])

        solr_query = self.solr.query(query)
        solr_query = solr_query.paginate(start=options['start'],
                                         rows=options['rows'])
        solr_response = solr_query.execute()

        return solr_response

    def _get_pages(self, url, total_results, start, rows):
        """
        Return list of paginated links.
        """
        # Generate links for all pages of results
        urls = self._pagination_urls(url, total_results, start, rows)
        url = get_ordered_url(url)
        pages = []
        # Truncate the links and add paging numbers
        if urls:
            try:
                url_index = urls.index(url)
                if url_index > 5:
                    start = url_index - 5
                    end = url_index + 5
                else:
                    start = 0
                    end = 10

                for page_url in urls[start: end]:
                    page = {
                        'index': urls.index(page_url),
                        'url': page_url
                    }

                    pages.append(page)
            except ValueError:
                pass

        return pages

    def _pagination_urls(self, url, total_results, start, rows):
        # Generate links for all pages of results
        urls = []
        url = get_ordered_url(url)
        for i in range(0, total_results, rows):
            params = {
                'start': i,
                'rows': rows,
            }
            page_url = add_url_params(url, params)
            urls.append(get_ordered_url(page_url))
        return urls

    def _get_first_page_url(self, url, total_results, start, rows):
        # Generate links for all pages of results
        urls = self._pagination_urls(url, total_results, start, rows)
        try:
            return urls[0]
        except IndexError:
            return None

    def _get_last_page_url(self, url, total_results, start, rows):
        # Generate links for all pages of results
        urls = self._pagination_urls(url, total_results, start, rows)
        try:
            last_page_url = urls[len(urls) - 1]
            return last_page_url
        except IndexError:
            return None

    def _solr_response_details(self, solr_response):
        """
        Return dictionary of meta information about solr response,
        such as number of found results, and number of paginated results.
        """
        details = {}
        results = solr_response.result.numFound

        if len(solr_response) > 10:
            details['rows'] = len(solr_response)
        else:
            details['rows'] = 10

        details['found'] = results
        details['start'] = solr_response.result.start
        details['end'] = details['start'] + len(solr_response)

        return details

    def get(self, request, *args, **kwargs):
        results = []
        context_data = {'wildcards': 0}
        options = self._parse_options(request)

        try:
            account = Account.objects.get(user=request.user)
            if account.expires > timezone.now():
                account_active = True
            else:
                account_active = False
        except Account.DoesNotExist:
            account_active = False
        except TypeError:  # non-logged users throw TypeError
            account_active = False

        if options.get('query', None) is not None:
            # Normalize
            options = self.validator.normalized(options)
            # Validate
            valid = self.validator.validate(options)
            valid, errors = self._validate_options(options)

            if not self.validator.validate(options):
                messages.error(request, 'Error: {}'.format(self.validator.errors))
                return render(request, self.template_name)

            solr_response = self._solr_query(options)
            details = self._solr_response_details(solr_response)
            results = list(solr_response)
            pages = self._get_pages(request.get_full_path(),
                                    details['found'],
                                    details['start'],
                                    details['rows'])
            first_page = self._get_first_page_url(request.get_full_path(),
                                                  details['found'],
                                                  details['start'],
                                                  details['rows'])
            last_page = self._get_last_page_url(request.get_full_path(),
                                                details['found'],
                                                details['start'],
                                                details['rows'])
            context_data = {'account_active': account_active,
                            'results': results,
                            'start': details['start'] + 1,  # human-facing count
                            'end': details['end'],
                            'wildcards': int(options['wildcards']),
                            'rows': details['rows'],
                            'pages': pages,
                            'first_page': first_page,
                            'last_page': last_page,
                            'found': details['found']}

        return render(request, self.template_name, context_data)
