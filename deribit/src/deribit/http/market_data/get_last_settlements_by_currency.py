# deribit/http/market_data/get_last_settlements_by_currency.py

from pydantic import BaseModel
from typing import Literal
from decimal import Decimal
from deribit.http.client import Client

class Settlement(BaseModel):
  funded: Decimal | None = None
  funding: Decimal | None = None
  index_price: Decimal | None = None
  instrument_name: str | None = None
  mark_price: Decimal | None = None
  position: Decimal | None = None
  profit_loss: Decimal | None = None
  session_bankruptcy: Decimal | None = None
  session_profit_loss: Decimal
  session_tax: Decimal | None = None
  session_tax_rate: Decimal | None = None
  socialized: Decimal | None = None
  timestamp: int
  type: Literal['settlement', 'delivery', 'bankruptcy']

class Result(BaseModel):
  continuation: str
  settlements: list[Settlement]

class GetLastSettlementsByCurrency:
  client: Client

  async def get_last_settlements_by_currency(self, currency: str, **params):
    r = await self.client.get('public/get_last_settlements_by_currency', params={'currency': currency, **params})
    return Result.model_validate(r.result)

