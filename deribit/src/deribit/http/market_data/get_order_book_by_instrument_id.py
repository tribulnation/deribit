# deribit/http/market_data/get_order_book_by_instrument_id.py

from deribit.http.client import Client
from .get_order_book import OrderBook

class GetOrderBookByInstrumentId:
  client: Client

  async def get_order_book_by_instrument_id(self, instrument_id: int, depth: int | None = None):
    params = {'instrument_id': instrument_id}
    if depth is not None:
      params['depth'] = depth
    r = await self.client.get('public/get_order_book_by_instrument_id', params=params)
    return OrderBook.model_validate(r.result)
