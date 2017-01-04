import logging
import requests


__VERSION__ = '0.0.1'
api_baseurl = 'https://api.squarespace.com'
api_version = '0.1'


class Squarespace(object):
    """Represents orders from a particular squarespace store.

    :api_key:
        Your Squarespace API key. Required.

    :api_baseurl:
        The baseuri for the Squarespace API. You shouldn't need to change
        this.

    :api_version:
        The version of the Squarespace API to target. If you change this
        without making any code changes you may break this library.
    """
    def __init__(self, api_key, api_baseurl=api_baseurl, api_version=api_version):
        self.api_key = api_key
        self.api_baseurl = api_baseurl
        self.api_version = api_version

        # Setup our HTTP session
        self.http = requests.Session()
        self.http.headers.update({'Authorization': 'Bearer ' + self.api_key})
        self.useragent = 'Squarespace python API v%s by Zach White.' % __VERSION__
        self._next_page = None

    @property
    def useragent(self):
        """Get the current useragent.
        """
        return self._useragent

    @useragent.setter
    def useragent(self, agent_string):
        """Set the User-Agent that will be used.
        """
        self._useragent = agent_string
        self.http.headers.update({'User-Agent': self._useragent})

    def get(self, path, args=None):
        """Retrieve an endpoint from the Squarespace API.
        """
        if not args:
            args = {}

        url = '%s/%s/%s' % (self.api_baseurl, self.api_version, path)
        logging.debug('url:%s args:%s', url, args)
        request = self.http.get(url, params=args)

        if request.status_code in [200, 201]:
            return request.json()
        elif request.status_code == 204:
            return True
        elif request.status_code == 401:
            raise ValueError('The API key %s is not valid.' % self.api_key)
        elif 200 < request.status_code < 299:
            logging.warning('Squarespace success response %s:' % request.status_code)
            logging.warning(request.text)
            raise NotImplementedError("Squarespace sent us a success response we're not prepared for!")
        elif 400 <= request.status_code < 499:
            logging.error('Squarespace error response %s:' % request.status_code)
            logging.error(request.text)
            raise RuntimeError("Squarespace thinks this request is bogus")
        elif 500 <= request.status_code < 599:
            logging.error('Squarespace error response %s:' % request.status_code)
            logging.error(request.text)
            raise RuntimeError("Squarespace is having problems, try later.")

        raise RuntimeError("An unknown error occurred fetching your request.")

    def order(self, order_id):
        """Retrieve a single order.
        """
        return self.get('commerce/orders/' + order_id)

    def orders(self, **args):
        """Retrieve the 20 latest orders, by modification date.
        """
        uri = 'commerce/orders'

        result = self.get(uri, args)
        self._next_page = result['pagination']['nextPageCursor'] if 'nextPageCursor' in result['pagination'] else None

        return result['result']

    def next_page(self):
        """Retrieve the next 20 orders, or None if there are no more orders.
        """
        return self.orders(cursor=self._next_page) if self._next_page else None

    def all_orders(self):
        orders = self.orders()

        while self._next_page:
            orders.extend(self.next_page())

        return orders

