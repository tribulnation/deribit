# deribit/http/market_data/get_delivery_prices.py

from datetime import date
from decimal import Decimal
from pydantic import BaseModel, RootModel
from deribit.http.client import Client

class DeliveryPriceEntry(BaseModel):
  date: date
  delivery_price: Decimal

class DeliveryPricesResult(BaseModel):
  data: list[DeliveryPriceEntry]
  records_total: int

class DeliveryPrices(RootModel):
  root: DeliveryPricesResult

class GetDeliveryPrices:
  client: Client

  async def get_delivery_prices(self, index_name: str, offset: int | None = None, count: int | None = None):
    params: dict = {'index_name': index_name}
    if offset is not None:
      params['offset'] = offset
    if count is not None:
      params['count'] = count
    r = await self.client.get('public/get_delivery_prices', params=params)
    return DeliveryPrices.model_validate(r.result).root
