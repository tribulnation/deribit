# deribit/http/market_data/get_order_book.py

from pydantic import BaseModel
from decimal import Decimal
from typing import Literal
from deribit.http.client import Client

class Stats(BaseModel):
  high: float | None = None
  low: float | None = None
  price_change: float | None = None
  volume: Decimal
  volume_usd: Decimal | None = None

class Greeks(BaseModel):
  delta: float
  gamma: float
  rho: float
  theta: float
  vega: float

class OrderBook(BaseModel):
  ask_iv: float | None = None
  asks: list[tuple[float, Decimal]]
  best_ask_amount: Decimal
  best_ask_price: float | None = None
  best_bid_amount: Decimal
  best_bid_price: float | None = None
  bid_iv: float | None = None
  bids: list[tuple[float, Decimal]]
  current_funding: float | None = None
  delivery_price: float | None = None
  funding_8h: float | None = None
  greeks: Greeks | None = None
  index_price: float
  instrument_name: str
  interest_rate: float | None = None
  last_price: float | None = None
  mark_iv: float | None = None
  mark_price: float
  max_price: float
  min_price: float
  open_interest: Decimal | None = None
  settlement_price: float | None = None
  state: Literal['open', 'closed']
  stats: Stats
  timestamp: int
  underlying_index: str | None = None
  underlying_price: float | None = None

class GetOrderBook:
  client: Client

  async def get_order_book(self, instrument_name: str, depth: int | None = None):
    params: dict = {'instrument_name': instrument_name}
    if depth is not None:
      params['depth'] = depth
    r = await self.client.get('public/get_order_book', params=params)
    return OrderBook.model_validate(r.result)
