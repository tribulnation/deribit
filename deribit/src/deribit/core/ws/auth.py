from typing_extensions import TypedDict
from dataclasses import dataclass, field
import asyncio
from uuid import uuid4
import hmac
import hashlib

def sign(data: bytes, *, secret: str):
  return hmac.new(secret.encode(), data, hashlib.sha256).hexdigest()

def signature_data(*, ts: int, nonce: str):
  return f'{ts}\n{nonce}\n'.encode()

from deribit.core import timestamp, AuthedClient, ApiResponse, validator, AuthError
from .base import Context, logger
from .client import SocketClient

class AuthData(TypedDict):
  access_token: str
  expires_in: int
  refresh_token: str
  scope: str

@dataclass
class AuthContext(Context):
  auth_data: AuthData
  refresher: asyncio.Task

AuthResponseT: type[AuthData] = AuthData # type: ignore
validate_auth_response = validator(AuthResponseT)

@dataclass
class AuthedSocketClient(SocketClient, AuthedClient):
  client_id: str
  client_secret: str = field(repr=False)

  @property
  async def ctx(self) -> AuthContext:
    if (ctx := getattr(self, '_ctx', None)) is None:
      ctx = await self.open()
      self._ctx = ctx
    return ctx

  async def login(self):
    ts = timestamp.now()
    nonce = uuid4().hex
    signature = sign(signature_data(ts=ts, nonce=nonce), secret=self.client_secret)
    r = await self.request('/public/auth', {
      'grant_type': 'client_signature',
      'signature': signature,
      'timestamp': ts,
      'nonce': nonce,
      'client_id': self.client_id,
    })
    if 'error' in r:
      raise AuthError(r)
    else:
      resp: AuthData = validate_auth_response(r['result']) if self.validate() else r['result']
      return resp

  async def open(self):
    ctx = await super().open()
    auth_data = await self.login()
    logger.info('Loging successful, token expires in %s seconds', auth_data['expires_in'])

    async def refresher(auth_data: AuthData):
      while True:
        await asyncio.sleep(auth_data['expires_in'] - 60)
        logger.info('Refreshing token')
        self._ctx.auth_data = auth_data = await self.login()
        logger.info('Token refreshed successfully. New token expires in %s seconds', auth_data['expires_in'])

    return AuthContext(
      auth_data=auth_data,
      refresher=asyncio.create_task(refresher(auth_data)),
      ws=ctx.ws,
      listener=ctx.listener,
    )
  
  async def authed_request(self, path: str, params=None) -> ApiResponse:
    ctx = await self.ctx
    return await self.req({
      'jsonrpc': '2.0',
      'method': path,
      'params': params,
      'access_token': ctx.auth_data['access_token'],
    })