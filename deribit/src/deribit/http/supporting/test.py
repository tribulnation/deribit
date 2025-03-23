from typing_extensions import Literal
from pydantic import BaseModel
from deribit.http.client import Client

class Result(BaseModel):
  version: str

class Test:
  client: Client

  async def test(self, throw: bool = False):
    params = {'expected_result': 'exception'} if throw else None
    r = await self.client.get('public/test', params=params)
    return Result.model_validate(r.result)

