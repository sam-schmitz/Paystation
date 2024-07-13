from paystation.domain import (linear_rate_strategy,
                               LinearRateStrategy,
                               progressive_rate_strategy,
                               AlternatingRateStrategy,
                               is_weekend,
                               Receipt
                               )


# Abstract Factories for PayStation variants
class AlphaTownFactory:

    config_id = "Alphatown"

    def create_rate_strategy(self):
        return LinearRateStrategy(150)

    def create_receipt(self, amt):
        return Receipt(amt)


class BetaTownFactory:

    config_id = "Betatown"

    def create_rate_strategy(self):
        return progressive_rate_strategy

    def create_receipt(self, amt):
        return Receipt(amt, barcode=True)


class TripoliFactory:

    config_id = "Tripoli"

    def create_rate_strategy(self):
        return LinearRateStrategy(200)

    def create_receipt(self, amt):
        return Receipt(amt)


class GammaTownFactory:

    config_id = "Gammatown"

    def create_rate_strategy(self):
        ars = AlternatingRateStrategy(is_weekend,
                                      progressive_rate_strategy,
                                      LinearRateStrategy(150))
        return ars

    def create_receipt(self, amt):
        return Receipt(amt)
