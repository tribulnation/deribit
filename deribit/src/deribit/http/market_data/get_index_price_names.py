# deribit/http/market_data/get_index_price_names.py

from pydantic import RootModel
from deribit.http.client import Client

class IndexPriceNames(RootModel):
  root: list[str]

class GetIndexPriceNames:
  client: Client

  async def get_index_price_names(self):
    r = await self.client.get('public/get_index_price_names')
    return IndexPriceNames.model_validate(r.result).root
