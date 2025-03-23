# deribit/http/market_data/ticker.py

from pydantic import BaseModel
from typing import Literal
from deribit.http.client import Client

class Greeks(BaseModel):
  delta: float
  gamma: float
  rho: float
  theta: float
  vega: float

class Stats(BaseModel):
  high: float | None = None
  low: float | None = None
  price_change: float | None = None
  volume: float
  volume_usd: float | None = None

class TickerResult(BaseModel):
  ask_iv: float | None = None
  best_ask_amount: float
  best_ask_price: float | None = None
  best_bid_amount: float
  best_bid_price: float | None = None
  bid_iv: float | None = None
  current_funding: float | None = None
  delivery_price: float | None = None
  estimated_delivery_price: float | None = None
  funding_8h: float | None = None
  greeks: Greeks | None = None
  index_price: float
  instrument_name: str
  interest_rate: float | None = None
  interest_value: float | None = None
  last_price: float | None = None
  mark_iv: float | None = None
  mark_price: float
  max_price: float
  min_price: float
  open_interest: float | None = None
  settlement_price: float | None = None
  state: Literal['open', 'closed']
  stats: Stats
  timestamp: int
  underlying_index: str | None = None
  underlying_price: float | None = None

class GetTicker:
  client: Client

  async def ticker(self, instrument_name: str) -> TickerResult:
    r = await self.client.get('public/ticker', params={'instrument_name': instrument_name})
    return TickerResult.model_validate(r.result)
