# coding=UTF-8
from squarespace import Squarespace


def test_squarespace():
    store = Squarespace('test')
    assert store.api_key == 'test'
    assert store.useragent == 'Squarespace python API v0.0.1 by Zach White.'


def test_squarespace_useragent():
    store = Squarespace('test')
    store.useragent = 'Hello, World!'
    assert store.useragent == 'Hello, World!'
    assert store._useragent == 'Hello, World!'
    assert store.http.headers['User-Agent'] == 'Hello, World!'
