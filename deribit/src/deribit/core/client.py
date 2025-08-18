from typing_extensions import TypedDict, NotRequired, Any, Self, AsyncIterable, Literal
from dataclasses import dataclass
from abc import ABC, abstractmethod
from .validation import validator, ValidationMixin

class BaseMessage(TypedDict):
  jsonrpc: str

class BaseResponse(BaseMessage):
  id: int
  testnet: bool
  usIn: int
  usOut: int
  usDiff: int

class OkResponse(BaseResponse):
  result: Any

class ApiError(TypedDict):
  code: int
  message: str
  data: NotRequired[Any|None]

class ErrorResponse(BaseResponse):
  error: ApiError

ApiResponse = OkResponse | ErrorResponse

ApiResponseT: type[ApiResponse] = ApiResponse # type: ignore
validate_response = validator(ApiResponseT)

class MessageParams(TypedDict):
  channel: str
  label: NotRequired[str|None]
  data: Any

class ApiNotification(BaseMessage):
  method: Literal['subscription']
  params: MessageParams

ApiMessage = ApiNotification | ApiResponse

ApiMessageT: type[ApiMessage] = ApiMessage # type: ignore
validate_message = validator(ApiMessageT)

DERIBIT_MAINNET = 'www.deribit.com'
DERIBIT_TESTNET = 'test.deribit.com'

@dataclass
class Client(ValidationMixin, ABC):
  @abstractmethod
  async def request(self, path: str, params=None, /) -> ApiResponse:
    ...

  @abstractmethod
  async def __aenter__(self) -> Self:
    ...
  
  @abstractmethod
  async def __aexit__(self, exc_type, exc_value, traceback):
    ...

class AuthedClient(Client):
  @abstractmethod
  async def authed_request(self, path: str, params=None, /) -> ApiResponse:
    ...

@dataclass(frozen=True)
class ClientMixin:
  client: Client

  async def request(self, path: str, params=None, /) -> ApiResponse:
    return await self.client.request(path, params)
  

@dataclass(frozen=True)
class AuthedClientMixin(ClientMixin):
  client: AuthedClient

  @abstractmethod
  async def authed_request(self, path: str, params=None, /) -> ApiResponse:
    ...