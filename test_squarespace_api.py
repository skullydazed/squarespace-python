# coding=UTF-8
# Make some live requsets with the squarespace API. To use this test you have
# to create a file called "api_key" in the current directory that contains
# your API key. You can generate a key by opening up your site's admin page
# (https://<yoursite>.squarespace.com/config/) and going to Settings ->
# Adnvarced -> API Keys.

import logging
from os.path import exists
from squarespace import Squarespace


api_key = open('api_key').read().strip() if exists('api_key') else None


def test_squarespace_api():
    if not api_key:
        logging.warning('Missing "api_key" file.')
        return True

    store = Squarespace(api_key)
    orders = store.orders()
    assert len(orders) > 0
    return True


def test_squarespace_api_pagination():
    if not api_key:
        logging.warning('Missing "api_key" file.')
        return True

    store = Squarespace(api_key)
    orders = store.orders()
    assert len(orders) == 20
    next = store.next_page()
    assert len(next) > 0
    assert orders[0]['id'] != orders[1]['id']
    return True

