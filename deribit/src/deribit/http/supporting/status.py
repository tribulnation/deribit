# deribit/http/supporting/status.py

from typing_extensions import Literal
from pydantic import BaseModel
from deribit.http.client import Client

class Result(BaseModel):
  locked: Literal['true', 'false', 'partial']
  locked_indices: list[str] = []

class Status:
  client: Client

  async def status(self):
    r = await self.client.get('public/status')
    return Result.model_validate(r.result)

