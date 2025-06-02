import decimal as dec
import operator

type Amount = int | str | dec.Decimal


class Currency:
    def __init__(self, data: dict, *, force: bool):  # unlock
        if not force:
            raise Exception  # TODO(d.burmistrov): . # noqa: TRY002

        self._data = data or {}

    def __call__(self, amount: Amount) -> "Money":
        return Money(amount=amount, currency=self)


class Money:  # slots?
    def __init__(self, amount: Amount, currency: Currency):
        self._currency = Currency(currency)  # validate currency
        self._amount = dec.Decimal(amount)

        # validate - is_nan / is_finite / ...
        if not (0 <= self._amount < dec.Decimal("Inf")):
            raise ValueError  # TODO(d.burmistrov): .

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency


class Wallet:  # FlexWallet / BanknoteWallet
    def __init__(self, *money: Money) -> None:
        self._pocket = dict()
        for m in money:
            self.__accept(m)

    @property
    def money(self):
        items = sorted(self._pocket.values(), key=operator.attrgetter("currencies"))
        return tuple(items)

    def __accept(self, money: Money) -> None:
        if money is self._pocket.setdefault(money.currency, money):
            return

        self._pocket[money.currency] += money


class Balance:
    def __init__(self, currency: Currency):
        self._currency = currency
        self._amount = 0

    @property
    def amount(self):
        return self._amount

    @property
    def currency(self):
        return self._currency

    def __extract_amount(self, money: Money):
        if money.currency is not self._currency:
            raise ValueError  # TODO(d.burmistrov): .

        return money.amount

    def credit(self, money: Money):
        self._amount += self.__extract_amount(money)

    def debit(self, money: Money):
        self._amount -= self.__extract_amount(money)


class Rates:
    pass


class Exchange:
    def __init__(self, rates: Rates):  # buy / sell
        pass
