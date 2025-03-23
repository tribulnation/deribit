from typing_extensions import Mapping, Any
from dataclasses import dataclass, field
import hmac
import hashlib
from uuid import uuid4
from urllib.parse import urlencode
from deribit.util import timestamp, path_join, getenv
from .client import Client, AuthedClient, Method

def sign(data: bytes, *, secret: str):
  return hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()

def str2sign(method: str, uri: str, body: str, ts: int, nonce: str):
  return f'{ts}\n{nonce}\n{method}\n{uri}\n{body}\n'

@dataclass
class HMACClient(AuthedClient):
  """Deribit HTTP client using HMAC authentication."""
  client_id: str = field(default_factory=getenv('DERIBIT_CLIENT_ID'), repr=False)
  client_secret: str = field(default_factory=getenv('DERIBIT_CLIENT_SECRET'), repr=False)

  def auth_header(
    self, *, method: str, uri: str, body: str | None = None,
    ts: int | None = None, nonce: str | None = None
  ):
    ts = ts or timestamp.now()
    nonce = nonce or uuid4().hex
    data = str2sign(method=method, uri=uri, ts=ts, nonce=nonce, body=body or '')
    signature = sign(data.encode(), secret=self.client_secret)
    return f'deri-hmac-sha256 id={self.client_id},ts={ts},sig={signature},nonce={nonce}'

  @Client.with_client
  async def authed_request(
    self, method: Method, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None, json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    uri = path_join(self.base_path, path)
    query = urlencode(params) if params else ''
    if query:
      uri += f'?{query}'
      path += f'?{query}'

    auth_header = self.auth_header(method=method, uri=uri, body=body)
    signed_headers = {
      'Authorization': auth_header,
      **(headers or {}),
    }
    return await self.request(method, path, body=body, json=json, headers=signed_headers, params=None)