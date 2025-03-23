# deribit/http/market_data/get_book_summary_by_currency.py

from typing import Literal, Union
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

Kind = Literal[
  'future', 'option', 'spot',
  'future_combo', 'option_combo'
]

class BookSummaryBase(BaseModel):
  ask_price: float | None = None
  base_currency: str
  bid_price: float | None = None
  creation_timestamp: int
  estimated_delivery_price: float | None = None
  high: float | None = None
  instrument_name: str
  last: float | None = None
  low: float | None = None
  mark_price: float | None = None
  mid_price: float | None = None
  open_interest: float | None = None
  price_change: float | None = None
  quote_currency: str
  underlying_index: str | None = None
  volume: float
  volume_notional: float | None = None
  volume_usd: float | None = None

class PerpBookSummary(BookSummaryBase):
  tag: Literal['perp'] = 'perp'
  current_funding: float
  funding_8h: float

class OptionBookSummary(BookSummaryBase):
  tag: Literal['option'] = 'option'
  interest_rate: float
  mark_iv: float
  underlying_price: float

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