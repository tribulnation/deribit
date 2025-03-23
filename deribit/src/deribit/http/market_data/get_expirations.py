from typing_extensions import Literal, overload, TypeVar, Any
from pydantic import BaseModel, RootModel
from deribit.http.client import Client
from deribit.util import Date

C = TypeVar('C', bound=str)

Kind = Literal['future', 'option', 'any']
Expiry = Date | Literal['PERPETUAL']

def lit(value: str):
  return Literal[value] # type: ignore

class FutureExpirations(BaseModel):
  future: list[Expiry]

class OptionExpirations(BaseModel):
  option: list[Expiry]

class AnyExpirations(BaseModel):
  future: list[Expiry]
  option: list[Expiry]

GroupedAnyExpirations = RootModel[dict[C, AnyExpirations]]
GroupedFutureExpirations = RootModel[dict[C, FutureExpirations]]
GroupedOptionExpirations = RootModel[dict[C, OptionExpirations]]

class GetExpirations:
  client: Client

  @overload
  async def get_expirations(self, currency: Literal['grouped'], kind: Literal['any'] = 'any') -> dict[str, AnyExpirations]: ...
  @overload
  async def get_expirations(self, currency: Literal['grouped'], kind: Literal['future']) -> dict[str, FutureExpirations]: ...
  @overload
  async def get_expirations(self, currency: Literal['grouped'], kind: Literal['option']) -> dict[str, OptionExpirations]: ...

  @overload
  async def get_expirations(self, currency: Literal['any'], kind: Literal['any'] = 'any') -> AnyExpirations: ...
  @overload
  async def get_expirations(self, currency: Literal['any'], kind: Literal['future']) -> FutureExpirations: ...
  @overload
  async def get_expirations(self, currency: Literal['any'], kind: Literal['option']) -> OptionExpirations: ...
  
  @overload
  async def get_expirations(self, currency: str, kind: Literal['any'] = 'any') -> AnyExpirations: ... # type: ignore
  @overload
  async def get_expirations(self, currency: str, kind: Literal['future']) -> FutureExpirations: ... # type: ignore
  @overload
  async def get_expirations(self, currency: str, kind: Literal['option']) -> OptionExpirations: ... # type: ignore

  async def get_expirations(self, currency: str, kind: Kind = 'any'): # type: ignore
    params = {'currency': currency, 'kind': kind}
    r = await self.client.get('public/get_expirations', params=params)
    if currency == 'grouped':
      if kind == 'any':
        return GroupedAnyExpirations[str].model_validate(r.result).root
      elif kind == 'future':
        return GroupedFutureExpirations[str].model_validate(r.result).root
      else:
        return GroupedOptionExpirations[str].model_validate(r.result).root
    
    elif currency == 'any':
      if kind == 'any':
        return AnyExpirations.model_validate(r.result)
      elif kind == 'future':
        return FutureExpirations.model_validate(r.result)
      else:
        return OptionExpirations.model_validate(r.result)

    else:
      if kind == 'any':
        return GroupedAnyExpirations[lit(currency)].model_validate(r.result).root[currency]
      elif kind == 'future':
        return GroupedFutureExpirations[lit(currency)].model_validate(r.result).root[currency]
      else:
        return GroupedOptionExpirations[lit(currency)].model_validate(r.result).root[currency]