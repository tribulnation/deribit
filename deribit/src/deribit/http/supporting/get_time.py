from pydantic import RootModel
from deribit.http.client import Client

class Result(RootModel):
  root: int

class GetTime:
  client: Client

  async def get_time(self):
    r = await self.client.get('public/get_time')
    return Result.model_validate(r.result).root

