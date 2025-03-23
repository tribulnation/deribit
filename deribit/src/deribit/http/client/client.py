from typing_extensions import Mapping, Literal, Any
from abc import ABC, abstractmethod
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
  _client: httpx.AsyncClient | None = field(default=None, init=False, kw_only=True)

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
    body: str | None = None, json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    r = await self.client.request(method, path, params=params, content=body, headers=headers, json=json)
    val = DeribitResponse.model_validate_json(r.text).root
    if val.error is not None:
      raise val.error
    return val
  
  async def get(
    self, path: str, *,
    params: Mapping[str, str|int] | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    return await self.request('GET', path, params=params, headers=headers)
  
  async def post(
    self, path: str, *,
    json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    return await self.request('POST', path, headers=headers, json={
      'jsonrpc': '2.0',
      'method': path,
      'params': json,
    })


class AuthedClient(ABC, Client):
  @abstractmethod
  async def authed_request(
    self, method: Method, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None, json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ) -> OkResponse:
    ...
  
  async def authed_get(
    self, path: str, *,
    params: Mapping[str, str|int] | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    return await self.authed_request('GET', path, params=params, headers=headers)
  
  async def authed_post(
    self, path: str, *, json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    return await self.authed_request('POST', path, headers=headers, json={
      'jsonrpc': '2.0',
      'method': path,
      'params': json,
    })

  @staticmethod
  def oauth2(
    *, client_id: str | None = None, client_secret: str | None = None,
    testnet: bool = False,
  ):
    kwargs = {'domain': DERIBIT_TESTNET if testnet else DERIBIT_MAINNET}
    if client_id is not None:
      kwargs['client_id'] = client_id
    if client_secret is not None:
      kwargs['client_secret'] = client_secret
    from .oauth2 import OAuth2Client
    return OAuth2Client(**kwargs)
  
  @staticmethod
  def hmac(
    *, client_id: str | None = None, client_secret: str | None = None,
    testnet: bool = False,
  ):
    kwargs = {'domain': DERIBIT_TESTNET if testnet else DERIBIT_MAINNET}
    if client_id is not None:
      kwargs['client_id'] = client_id
    if client_secret is not None:
      kwargs['client_secret'] = client_secret
    from .hmac import HMACClient
    return HMACClient(**kwargs)