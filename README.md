# squarespace-python

Python module to access the Squarespace Commerce API.

This library provides pythonic access to the Squarespace Commerce API that
can be found here:

    http://developers.squarespace.com/commerce-api

At the time of this writing this API is in private beta and therefore
your store may not have the ability to generate API keys.

## Usage

    from squarespace import Squarespace

    store = Squarespace('<my_api_key_that_I_generated>')
    for order in store.orders(): # Iterate through 20 orders
        print(order['order_number'])
    for order in store.next_page(): # Iterate through another 20 orders
        print(order['order_number'])

## Installation

    `$ pip install squarespace`

## Disclaimer

This project's author is not employed by or affiliated with Squarespace 
beyond being a happy customer who wanted to write his own shipping 
integration. Use of this software is entirely at your own risk. Neither 
Zach White, Clueboard, nor Squarespace can be held responsible for how
you employ this module.
