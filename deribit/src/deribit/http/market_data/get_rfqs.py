# deribit/http/market_data/get_rfqs.py

from pydantic import BaseModel
from typing import Literal
from decimal import Decimal
from deribit.http.client import Client

class RFQ(BaseModel):
  amount: Decimal
  instrument_name: str
  last_rfq_timestamp: int
  side: Literal['buy', 'sell']
  traded_volume: Decimal

class GetRFQs:
  client: Client

  async def get_rfqs(self, currency: str, kind: str | None = None) -> list[RFQ]:
    params = {'currency': currency}
    if kind:
      params['kind'] = kind
    r = await self.client.get('public/get_rfqs', params=params)
    return [RFQ.model_validate(x) for x in r.result]
