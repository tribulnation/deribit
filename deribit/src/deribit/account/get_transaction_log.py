from typing_extensions import TypedDict, Literal, NotRequired, Union, Annotated
from dataclasses import dataclass
from decimal import Decimal
from datetime import datetime
from pydantic import Discriminator, Tag

from deribit.core import AuthedClientMixin, ApiResponse, validator, timestamp as ts

class TransferInfo(TypedDict):
  transaction: str
  addr: str

class BaseTransfer(TypedDict):
  timestamp: int
  id: int
  currency: str
  commission: Decimal
  info: TransferInfo

class Withdrawal(BaseTransfer):
  type: Literal['withdrawal']

class Deposit(BaseTransfer):
  type: Literal['deposit']

class Other(TypedDict):
  type: str

def discriminator(v) -> str:
  if v.get('type') in ['deposit', 'withdrawal']:
    return v['type']
  else:
    return 'other'
  
Transaction = Annotated[
  Union[
    Annotated[Deposit, Tag('deposit')],
    Annotated[Withdrawal, Tag('withdrawal')],
    Annotated[Other, Tag('other')],
  ],
  Discriminator(discriminator)
]

class TransactionLog(TypedDict):
  continuation: NotRequired[int|None]
  logs: list[Transaction]

validate_response = validator(TransactionLog)

Query = Literal['deposit', 'withdrawal']

@dataclass(frozen=True)
class GetTransactionLog(AuthedClientMixin):
  async def get_transaction_log(
    self, currency: str, *,
    start: datetime, end: datetime,
    query: Query | str | None = None,
    subaccount_id: str | None = None,
    count: int | None = None,
    continuation: int | None = None,
    validate: bool = True
  ) -> ApiResponse[TransactionLog]:
    """Places a buy order for an instrument.
    
    - `currency`: The currency to get the transaction log for.
    - `start`: The start timestamp to get the transaction log for.
    - `end`: The end timestamp to get the transaction log for.
    - `query`: Query to filter results. See the [docs](https://docs.deribit.com/#private-get_transaction_log) for details.
    - `subaccount_id`: The subaccount id to get the transaction log for.
    - `count`: Number of requested items (default: 100, max: 250).
    - `continuation`: The continuation token to get the next page of results.
    - `validate`: Whether to validate the response against the expected schema.
    
    > [Deribit API docs](https://docs.deribit.com/#private-get_transaction_log)
    """
    params: dict = {'currency': currency}
    if subaccount_id is not None:
      params['subaccount_id'] = subaccount_id
    if query is not None:
      params['query'] = query
    if start is not None:
      params['start_timestamp'] = ts.dump(start)
    if end is not None:
      params['end_timestamp'] = ts.dump(end)
    if count is not None:
      params['count'] = count
    if continuation is not None:
      params['continuation'] = continuation
    r = await self.authed_request('/private/get_transaction_log', params)
    if self.validate(validate) and 'result' in r:
      r['result'] = validate_response(r['result'])
    return r
    