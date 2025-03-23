# deribit/http/market_data/get_index_price.py

from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class IndexPriceResult(BaseModel):
  estimated_delivery_price: Decimal
  index_price: Decimal

class IndexPriceResponse(RootModel):
  root: IndexPriceResult

class GetIndexPrice:
  client: Client

  async def get_index_price(self, index_name: str):
    r = await self.client.get('public/get_index_price', params={'index_name': index_name})
    return IndexPriceResponse.model_validate(r.result).root


