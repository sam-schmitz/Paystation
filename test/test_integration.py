# test_integration.py

import unittest


from paystation.domain import (PayStation,
                               is_weekend,
                               progressive_rate_strategy,
                               LinearRateStrategy,
                               linear_rate_strategy
                               )
from paystation.config import (AlphaTownFactory,
                               BetaTownFactory,
                               GammaTownFactory,
                               TripoliFactory
                               )


def insert_coins(ps, coins):
    for coin in coins:
        ps.add_payment(coin)


class TestAlphaTownIntegration(unittest.TestCase):

    def setUp(self):
        self.ps = PayStation(AlphaTownFactory())
        self.ps.add_payment(25)

    def test_paystation_linear_rate(self):
        self.assertEqual(25//5*2, self.ps.read_display())

    def test_std_receipt(self):
        rec = self.ps.buy()
        self.assertFalse(rec.with_barcode)


class TestBetaTownIntegration(unittest.TestCase):

    def setUp(self):
        self.ps = PayStation(BetaTownFactory())

    def test_paystation_progressive_rate(self):
        insert_coins(self.ps, [25, 25, 25, 25, 25, 25])
        self.assertEqual(150//5*2, self.ps.read_display())
        insert_coins(self.ps, [25, 25, 25, 25, 25, 25, 25, 25])
        self.assertEqual(150//5*2+200//5*1.5, self.ps.read_display())
        insert_coins(self.ps, [25])
        self.assertEqual(150//5*2 + 200//5*1.5 + 25//5, self.ps.read_display())

    def test_barcode_receipt(self):
        self.ps.add_payment(25)
        rec = self.ps.buy()
        self.assertTrue(rec.with_barcode)


class TestGammaTownIntegration(unittest.TestCase):

    def setUp(self):
        self.ps = PayStation(GammaTownFactory())

    def test_paystion_alternating_rate(self):
        insert_coins(self.ps, [25]*12)
        if is_weekend():
            self.assertEqual(progressive_rate_strategy(25*12),
                             self.ps.read_display())
        else:
            self.assertEqual(linear_rate_strategy(25*12),
                             self.ps.read_display())

    def test_std_receipt(self):
        self.ps.add_payment(25)
        rec = self.ps.buy()
        self.assertFalse(rec.with_barcode)


class TestTripoliIntegration(unittest.TestCase):

    def setUp(self):
        self.ps = PayStation(TripoliFactory())
        self.ps.add_payment(25)

    def test_paystation_new_linear_rate(self):
        rate = LinearRateStrategy(200)
        self.assertEqual(round(rate(25)), self.ps.read_display())

    def test_std_receipt(self):
        rec = self.ps.buy()
        self.assertFalse(rec.with_barcode)
