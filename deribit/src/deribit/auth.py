from dataclasses import dataclass
from pydantic import BaseModel
from datetime import datetime, timedelta
from .client import SocketClient, DERIBIT_MAINNET

class AuthResponse(BaseModel):
  access_token: str
  expires_in: int
  refresh_token: str
  scope: str

class AuthData(AuthResponse):
  expires_at: datetime

@dataclass
class PrivateClient:
  client_id: str
  client_secret: str
  client: SocketClient

  @classmethod
  def new(cls, client_id: str, client_secret: str, *, url: str | None = None, timeout_secs: int | None = None):
    client = SocketClient(url=url, timeout_secs=timeout_secs)
    return cls(client_id, client_secret, client)

  async def authenticate(self):
    r = await self.client.request({
      'method': 'public/auth',
      'params': {
        'grant_type': 'client_credentials',
        'client_id': self.client_id,
        'client_secret': self.client_secret
      }
    })
    auth = AuthResponse.model_validate(r)
    expires_at = datetime.now() + timedelta(seconds=auth.expires_in)
    return AuthData(expires_at=expires_at, **auth.model_dump())
  
  # TODO
  async def refresh_token(self):
    ...

  async def request(self, msg: dict):
    return await self.client.request(msg)
  
  async def __aenter__(self):
    await self.client.__aenter__()
    auth = await self.authenticate()
    return AuthedClient(self, auth)
  
  async def __aexit__(self, *args):
    await self.client.__aexit__(*args)

@dataclass
class AuthedClient:
  client: PrivateClient
  auth: AuthResponse  

  # TODO: check whether `self.auth.expires_at < datetime.now() - timedelta(seconds=5)`
  async def authed_request(self, msg: dict) -> dict:
    return await self.client.request({'access_token': self.auth.access_token, **msg})