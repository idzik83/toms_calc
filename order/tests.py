from django.test import TestCase
from django.urls import reverse
from parameterized import parameterized
from rest_framework.test import APITestCase, APIClient

from .utils import OrderCalculator


class OrderCalculatorTestCase(TestCase):

    @parameterized.expand([
        (10, 5, 'tx', 50),
        (100, 10, 'tx', 970),
        (4999, 1, 'tx', 4849.03),
        (600, 10, 'tx', 5700),
        (3617.21, 2, 'tx', 6728.01),
        (3213, 25, 'tx', 68276.25),
    ])
    def test_discounted_price(self, price, quantity, state_code, expected_discount_price):
        calculator = OrderCalculator(price, quantity, state_code)
        self.assertEqual(calculator.discounted_price, expected_discount_price)

    @parameterized.expand([
        (500, 3, 'ut', 1554.67),
        (1841, 3, 'nv', 5666.6),
        (1473, 5, 'tx', 7277.54),
        (3000, 7, 'al', 19656),
        (50000, 3, 'ca', 138018.75),
    ])
    def test_taxed_price(self, price, quantity, state_code, expected_discount_price):
        calculator = OrderCalculator(price, quantity, state_code)
        self.assertEqual(calculator.taxed_price, expected_discount_price)

    def test_value_error(self):
        with self.assertRaises(ValueError):
            calculator = OrderCalculator(1, 2, 'fake state')
            _ = calculator.taxed_price


class TestTotalOrderPrice(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('order:order-price-handler')

    @parameterized.expand([
        ([dict(price=1000, quantity=15, state_code='fake')]),
        ([dict(price=-1000, quantity=15, state_code='tx')]),
        ([dict(price=1000, quantity=0, state_code='tx')]),
    ])
    def test_bad_request(self, payload):
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 400)

    def test_positive_flow(self):
        expected_total = 1030.62
        payload = ({'price': 100, 'quantity': 10, 'state_code': 'tx'})
        response = self.client.post(self.url, data=payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['total'], expected_total)
