from typing_extensions import Mapping, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pydantic import BaseModel
from deribit.util import getenv
from .client import Client, AuthedClient, Method

class AuthResponse(BaseModel):
  access_token: str
  expires_in: int
  refresh_token: str
  scope: str

class AuthData(AuthResponse):
  expires_at: datetime

@dataclass
class OAuth2Client(AuthedClient):
  client_id: str = field(default_factory=getenv('DERIBIT_CLIENT_ID'), kw_only=True, repr=False)
  client_secret: str = field(default_factory=getenv('DERIBIT_CLIENT_SECRET'), kw_only=True, repr=False)
  auth: AuthData | None = field(default=None, init=False)

  @Client.with_client
  async def access_token(self):
    if self.auth is None:
      self.auth = await self.authenticate()
    elif datetime.now() >= self.auth.expires_at:
      self.auth = await self.refresh(self.auth.refresh_token)
    return self.auth.access_token

  @Client.with_client
  async def authenticate(self):
    r = await self.request('GET', 'public/auth', params={
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'grant_type': 'client_credentials',
    })
    auth = AuthResponse.model_validate(r.result)
    expires_at = datetime.now() + timedelta(seconds=auth.expires_in)
    return AuthData(expires_at=expires_at, **auth.model_dump())
  
  @Client.with_client
  async def refresh(self, refresh_token: str):
    r = await self.request('GET', 'public/auth', params={
      'client_id': self.client_id,
      'client_secret': self.client_secret,
      'grant_type': 'refresh_token',
      'refresh_token': refresh_token,
    })
    auth = AuthResponse.model_validate(r.result)
    expires_at = datetime.now() + timedelta(seconds=auth.expires_in)
    self.auth = AuthData(expires_at=expires_at, **auth.model_dump())
    return self.auth
  
  @Client.with_client
  async def authed_request(
    self, method: Method, path: str, *,
    params: Mapping[str, str|int] | None = None,
    body: str | None = None, json: Any | None = None,
    headers: Mapping[str, str] | None = None,
  ):
    access_token = await self.access_token()
    return await self.request(method, path, params=params, body=body, json=json, headers={
      'Authorization': f'Bearer {access_token}',
      **(headers or {}),
    })
  