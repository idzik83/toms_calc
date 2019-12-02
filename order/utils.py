from collections import namedtuple
from operator import ge


StateTaxRate = namedtuple('StateTaxRate', ['name', 'code', 'tax_rate'])
Discount = namedtuple('Discount', ['limit', 'condition', 'discount'])

States = (
    StateTaxRate('UT', 'ut', 0.0685),
    StateTaxRate('NV', 'nv', 0.08),
    StateTaxRate('TX', 'tx', 0.0625),
    StateTaxRate('AL', 'al', 0.04),
    StateTaxRate('CA', 'ca', 0.0825)
)

Discounts = (
    Discount(1000, ge, 0.03),
    Discount(5000, ge, 0.05),
    Discount(7000, ge, 0.07),
    Discount(10000, ge, 0.1),
    Discount(50000, ge, 0.15)
)


class OrderCalculator:
    def __init__(self, price: float, quantity: int, state_code: str):
        self._price = price
        self._qty = quantity
        self._state_code = state_code
        self._total = self._price * self._qty
        self._tax_map = {state.code: state.tax_rate for state in States}
        self._discounted_price = None
        self._taxed_price = None

    @property
    def discounted_price(self) -> float:
        return self._discounted_price or self._get_discounted_price()

    @property
    def taxed_price(self) -> float:
        return self._taxed_price or self._get_taxed_price()

    def _get_discounted_price(self) -> float:
        for discount in reversed(Discounts):
            if discount.condition(self._total, discount.limit):
                self._discounted_price = round(self._total * (1 - discount.discount), 2)
                return self._discounted_price
        return self._total

    def _get_taxed_price(self) -> float:
        tax_rate = self._tax_map.get(self._state_code)
        if not tax_rate:
            raise ValueError(f'Tax for {self._state_code} is not registered')
        self._taxed_price = round(self.discounted_price * (1 + tax_rate), 2)
        return self._taxed_price
