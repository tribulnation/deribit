# deribit/http/market_data/get_supported_index_names.py

from deribit.http.client import Client

class GetSupportedIndexNames:
  client: Client

  async def get_supported_index_names(self, type: str | None = None) -> list[str]:
    r = await self.client.get('public/get_supported_index_names', params={'type': type} if type else None)
    return r.result
