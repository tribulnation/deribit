# deribit/http/market_data/get_last_trades_by_currency.py

from typing import Literal
from pydantic import BaseModel
from decimal import Decimal
from deribit.http.client import Client

class Trade(BaseModel):
  amount: Decimal
  block_rfq_id: int | None = None
  block_trade_id: str | None = None
  block_trade_leg_count: int | None = None
  combo_id: str | None = None
  combo_trade_id: int | None = None
  contracts: Decimal | None = None
  direction: Literal['buy', 'sell']
  index_price: float
  instrument_name: str
  iv: float | None = None
  liquidation: str | None = None
  mark_price: float
  price: float
  tick_direction: int
  timestamp: int
  trade_id: str
  trade_seq: int

class Result(BaseModel):
  has_more: bool
  trades: list[Trade]

class GetLastTradesByCurrency:
  client: Client

  async def get_last_trades_by_currency(self, currency: str, **params):
    r = await self.client.get('public/get_last_trades_by_currency', params={'currency': currency, **params})
    return Result.model_validate(r.result)
