# deribit/http/market_data/get_index.py

from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class IndexResult(BaseModel):
  BTC: Decimal | None = None
  ETH: Decimal | None = None
  edp: Decimal | None = None

class IndexResponse(RootModel):
  root: IndexResult

class GetIndex:
  client: Client

  async def get_index(self, currency: str):
    r = await self.client.get('public/get_index', params={'currency': currency})
    return IndexResponse.model_validate(r.result).root


