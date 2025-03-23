# deribit/http/market_data/__init__.py

from dataclasses import dataclass
from deribit.http.client import Client
from .get_book_summary_by_currency import GetBookSummaryByCurrency
from .get_book_summary_by_instrument import GetBookSummaryByInstrument
from .get_contract_size import GetContractSize
from .get_currencies import GetCurrencies
from .get_delivery_prices import GetDeliveryPrices

@dataclass
class MarketData(
  GetBookSummaryByCurrency, GetBookSummaryByInstrument, GetContractSize, GetCurrencies,
  GetDeliveryPrices
):
  client: Client