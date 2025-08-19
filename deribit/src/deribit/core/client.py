from typing_extensions import TypedDict, NotRequired, Any, Self, Literal, TypeVar, Generic
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from .validation import validator, ValidationMixin

T = TypeVar('T', default=Any)

class BaseResponse(TypedDict):
  jsonrpc: str

class OkResponse(BaseResponse, Generic[T]):
  result: T

class ApiError(TypedDict):
  code: int
  message: str
  data: NotRequired[Any|None]

class ErrorResponse(BaseResponse):
  error: ApiError

ApiResponse = OkResponse[T] | ErrorResponse

ApiResponseT: type[ApiResponse] = ApiResponse # type: ignore
validate_response = validator(ApiResponseT)

DERIBIT_MAINNET = 'www.deribit.com'
DERIBIT_TESTNET = 'test.deribit.com'

@dataclass
class Client(ABC):
  validate: bool = field(kw_only=True, default=True)

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
class ClientMixin(ValidationMixin):
  client: Client

  async def request(self, path: str, params=None, /) -> ApiResponse:
    return await self.client.request(path, params)
  

@dataclass(frozen=True)
class AuthedClientMixin(ClientMixin):
  client: AuthedClient

  async def authed_request(self, path: str, params=None, /) -> ApiResponse:
    return await self.authed_request(path, params)