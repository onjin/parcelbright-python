#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_parcelbright
----------------------------------

Tests for `parcelbright` module.
"""

import os
import unittest

import parcelbright


class TestParcelBright(unittest.TestCase):

    def test_container_parcel(self):
        p = parcelbright.Parcel(
            width=10, height=10, length=10, weight=1
        )
        self.assertEqual(p.dict(), {
            'width': 10, 'height': 10, 'length': 10, 'weight': 1,
        })

    def test_container_parcel_with_protected_fields(self):
        p = parcelbright.Parcel(
            width=10, height=10, length=10, weight=1
        )
        p._protected = True
        p.__private = True
        self.assertEqual(p.dict(), {
            'width': 10, 'height': 10, 'length': 10, 'weight': 1,
        })

    def test_container_address(self):
        a = parcelbright.Address(
            name='office', postcode='AAA AAA', town='London',
            phone='12341234', country_code='GB', line1='line'
        )
        self.assertEqual(a.dict(), {
            'name': 'office', 'postcode': 'AAA AAA', 'town': 'London',
            'phone': '12341234', 'country_code': 'GB', 'line1': 'line'
        })

    @unittest.skipUnless(
        'PARCELBRIGHT_TEST_API_KEY' in os.environ,
        """Skip integrations test unless environment variable
        PARCELBRIGHT_TEST_API_KEY is not set"""
    )
    def test_rate(self):
        parcelbright.api_key = os.environ.get('PARCELBRIGHT_TEST_API_KEY')
        parcelbright.sandbox = True
        parcel = parcelbright.Parcel(
            length=10, width=10, height=10, weight=1
        )
        from_address = parcelbright.Address(
            name="office", postcode="NW1 0DU",
            town="London", phone="07800000000",
            line1="19 Mandela Street",
            country_code="GB"
        )
        to_address = parcelbright.Address(
            name="John Doe", postcode="E2 8RS",
            town="London", phone="07411111111",
            line1="19 Mandela Street",
            country_code="GB"
        )
        shipment = parcelbright.Shipment.create(
            customer_reference='123455667', estimated_value=100,
            contents='books', pickup_date='2025-01-29',
            parcel=parcel, from_address=from_address,
            to_address=to_address
        )
        self.assertTrue(isinstance(shipment.rates, list))

        found_shipment = parcelbright.Shipment.find(shipment.id)
        self.assertEqual(shipment.id, found_shipment.id)

        with self.assertRaises(parcelbright.NotFound):
            parcelbright.Shipment.find('invalid')

        found_shipment.book(found_shipment.rates[0]['code'])
        self.assertIn('label', found_shipment.__dict__)


if __name__ == '__main__':
    unittest.main()