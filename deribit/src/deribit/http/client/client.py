from typing_extensions import Mapping, Literal, Any, Protocol
from dataclasses import dataclass, field
from functools import wraps
from pydantic import BaseModel, RootModel
import httpx

DERIBIT_TESTNET = 'test.deribit.com'
DERIBIT_MAINNET = 'www.deribit.com'

Method = Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS', 'HEAD', 'TRACE']

@dataclass
class DeribitError(Exception):
  code: int
  message: str
  data: dict | None = None

  def __str__(self) -> str:
    return repr(self)

class _BaseResponse(BaseModel):
  jsonrpc: str
  testnet: bool
  usIn: int
  usOut: int
  usDiff: int

class OkResponse(_BaseResponse):
  result: Any
  error: None = None

class ErrorResponse(_BaseResponse):
  result: None = None
  error: DeribitError

class DeribitResponse(RootModel):
  root: OkResponse | ErrorResponse

@dataclass
class Client:
  domain: str = field(default=DERIBIT_MAINNET, kw_only=True)
  base_path: str = field(default='/api/v2/', kw_only=True)
  _client: httpx.AsyncClient | None = field(default=None, repr=False, kw_only=True)

  @property
  def base(self):
    return f"https://{self.domain}{self.base_path}"

  @classmethod
  def testnet(cls):
    return cls(domain=DERIBIT_TESTNET)

  async def __aenter__(self):
    self._client = httpx.AsyncClient(base_url=self.base)
    return self
  
  async def __aexit__(self, *_):
    if self._client is not None:
      await self._client.aclose()
      self._client = None

  @property
  def client(self) -> httpx.AsyncClient:
    if self._client is None:
      raise RuntimeError('Please use as context manager: `async with ...: ...`')
    return self._client
  
  @staticmethod
  def with_client(fn):
    @wraps(fn)
    async def wrapper(self, *args, **kwargs):
      if self._client is None:
        async with self:
          return await fn(self, *args, **kwargs)
      else:
        return await fn(self, *args, **kwargs)
      
    return wrapper
  
  @with_client
  async def request(
    self, method: Method, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    r = await self.client.request(method, path, params=params, content=body, headers=headers)
    val = DeribitResponse.model_validate_json(r.text).root
    if val.error is not None:
      raise val.error
    return val
  
  async def get(
    self, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    return await self.request('GET', path, params=params, body=body, headers=headers)


class AuthedClient(Protocol):
  async def authed_request(
    self, method: Method, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None,
    headers: Mapping[str, str] | None = None,
  ) -> OkResponse:
    ...
