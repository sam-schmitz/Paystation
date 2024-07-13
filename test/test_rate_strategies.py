# test_rate_strategies.py

import unittest
from unittest.mock import Mock

from paystation.domain import (linear_rate_strategy,
                               LinearRateStrategy,
                               progressive_rate_strategy,
                               AlternatingRateStrategy,
                               is_weekend
                               )


class TestLinearRate(unittest.TestCase):

    def test_correct_value_for_100_cents(self):
        # using "old-fashioned" linear_rate_strategy
        lrs = linear_rate_strategy
        self.assertEqual(100 // 5 * 2, lrs(100))

    def test_150_gets_one_hour(self):
        # using new LinearRateStrategy class
        lrs = LinearRateStrategy(150)
        self.assertEqual(60, lrs(150))

    def test_200_gets_one_hour(self):
        lrs = LinearRateStrategy(200)
        self.assertEqual(60, lrs(200))


class TestProgressiveRate(unittest.TestCase):

    def setUp(self):
        self.rate = progressive_rate_strategy

    def test_correct_value_for_150_cents(self):
        self.assertEqual(150//5*2, self.rate(150))

    def test_correct_value_for_100_cents(self):
        self.assertEqual(100//5*2, self.rate(100))

    def test_correct_value_for_350_cents(self):
        self.assertEqual(150//5*2+200//5*1.5, self.rate(350))

    def test_correct_value_for_200_cents(self):
        self.assertEqual((350-200)//5*2+50//5*1.5, self.rate(200))

    def test_correct_value_for_650_cents(self):
        self.assertEqual((150)//5*2 + 200//5*1.5 + 300//5, self.rate(650))

    def test_correct_value_for_400_cents(self):
        self.assertEqual((350-200)//5*2+200//5*1.5 + 50//5, self.rate(400))

    def test_correct_value_for_700_cents(self):
        self.assertEqual((350-200)//5*2+200//5*1.5 + 350//5, self.rate(700))


class TestAlternatingRateStrategy(unittest.TestCase):

    def fake_rate_strategy_always_30(self, amount):
        return 30

    def fake_rate_strategy_always_60(self, amount):
        return 60

    def setUp(self):
        self.decision_strategy = Mock()
        self.ars = AlternatingRateStrategy(self.decision_strategy,
                                           self.fake_rate_strategy_always_30,
                                           self.fake_rate_strategy_always_60
                                           )

    def test_uses_correct_strategy_on_weekend(self):
        self.decision_strategy.return_value = True
        self.assertEqual(30, self.ars(500))

    def test_uses_correct_strategy_on_weekday(self):
        self.decision_strategy.return_value = False
        self.assertEqual(60, self.ars(500))

    def test_is_weekend_returns_boolean(self):
        self.assertIn(is_weekend(), [True, False])
