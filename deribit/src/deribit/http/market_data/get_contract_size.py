# deribit/http/market_data/get_contract_size.py

from pydantic import BaseModel, field_validator
from decimal import Decimal
from deribit.http.client import Client

class Result(BaseModel):
  contract_size: Decimal

class GetContractSize:
  client: Client

  async def get_contract_size(self, instrument_name: str) -> Decimal:
    r = await self.client.get('public/get_contract_size', params={
      'instrument_name': instrument_name
    })
    return Result.model_validate(r.result).contract_size
