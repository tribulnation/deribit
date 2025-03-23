# deribit/http/market_data/get_book_summary_by_instrument.py

from pydantic import RootModel
from deribit.http.client import Client
from deribit.http.market_data.get_book_summary_by_currency import BookSummary

class BookSummaryList(RootModel):
  root: list[BookSummary]

class GetBookSummaryByInstrument:
  client: Client

  async def get_book_summary_by_instrument(self, instrument_name: str):
    r = await self.client.get('public/get_book_summary_by_instrument', params={
      'instrument_name': instrument_name
    })
    return BookSummaryList.model_validate(r.result).root
