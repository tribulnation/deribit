# deribit/http/market_data/get_book_summary_by_currency.py

from typing import Literal, Union
from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

Kind = Literal[
  'future', 'option', 'spot',
  'future_combo', 'option_combo'
]

class BookSummaryBase(BaseModel):
  ask_price: Decimal | None = None
  base_currency: str
  bid_price: Decimal | None = None
  creation_timestamp: int
  estimated_delivery_price: Decimal | None = None
  high: Decimal | None = None
  instrument_name: str
  last: Decimal | None = None
  low: Decimal | None = None
  mark_price: Decimal | None = None
  mid_price: Decimal | None = None
  open_interest: Decimal | None = None
  price_change: Decimal | None = None
  quote_currency: str
  underlying_index: str | None = None
  volume: Decimal
  volume_notional: Decimal | None = None
  volume_usd: Decimal | None = None

class PerpBookSummary(BookSummaryBase):
  tag: Literal['perp'] = 'perp'
  current_funding: Decimal
  funding_8h: Decimal

class OptionBookSummary(BookSummaryBase):
  tag: Literal['option'] = 'option'
  interest_rate: Decimal
  mark_iv: Decimal
  underlying_price: Decimal

class OtherBookSummary(BookSummaryBase):
  tag: None = None

BookSummary = Union[PerpBookSummary, OptionBookSummary, OtherBookSummary]

class BookSummaryList(RootModel):
  root: list[BookSummary]

class GetBookSummaryByCurrency:
  client: Client

  async def get_book_summary_by_currency(self, currency: str, kind: Kind | None = None):
    params = {'currency': currency}
    if kind:
      params['kind'] = kind
    r = await self.client.get('public/get_book_summary_by_currency', params=params)
    return BookSummaryList.model_validate(r.result).root