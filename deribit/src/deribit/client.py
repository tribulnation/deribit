from typing_extensions import Any
import asyncio
import json
from dataclasses import dataclass, field
import websockets
from pydantic import BaseModel

DERIBIT_TESTNET = "wss://test.deribit.com/ws/api/v2"
DERIBIT_MAINNET = "wss://www.deribit.com/ws/api/v2"

@dataclass
class DeribitError(Exception):
  code: int
  message: str
  data: dict | None = None

  def __str__(self) -> str:
    return repr(self)

class DeribitResponse(BaseModel):
  jsonrpc: str
  id: int
  result: Any | None = None
  error: DeribitError | None = None

@dataclass
class SocketClient:
  url: str | None = field(default=None, kw_only=True)
  timeout_secs: int | None = field(default=None, kw_only=True)
  debug: bool = field(default=False, kw_only=True)
  _id: int = field(default=0, init=False)
  _subscribers: dict[int, asyncio.Future[DeribitResponse]] = field(default_factory=dict, init=False)
  _socket: websockets.ClientConnection | None = field(default=None, kw_only=True)
  _listener: asyncio.Task | None = field(default=None, init=False)

  async def __aenter__(self):
    url = self.url or DERIBIT_MAINNET
    if self.debug:
      print(f'Connecting to {url}')
    self._socket = await websockets.connect(url).__aenter__()
    if self.debug:
      print('Starting listener task')
    self._listener = asyncio.create_task(self.listener())
    return self
  
  async def __aexit__(self, *args):
    if self._listener is not None:
      if self.debug:
        print('Canceling listener')
      self._listener.cancel()
      self._listener = None
    if self._socket is not None:
      if self.debug:
        print('Closing socket')
      await self._socket.__aexit__(*args)
      self._socket = None

  @property
  def socket(self) -> websockets.ClientConnection:
    client = getattr(self, '_socket', None)
    if client is None:
      raise RuntimeError('Please use as context manager: `async with ...: ...`')
    return client
  
  async def listener(self):
    try:
      while True:
        data = await self.socket.recv()
        if self.debug:
          print('Received message:', data)
        msg = DeribitResponse.model_validate_json(data)
        future = self._subscribers.get(msg.id)
        if self.debug:
          print(f'Notifying future [id = {msg.id}]:', future)
        if future is not None:
          future.set_result(msg)
          del self._subscribers[msg.id]
    except asyncio.CancelledError:
      ...
    except:
      import traceback
      traceback.print_exc()

  async def request(self, msg: dict):
    self._id += 1
    id = self._id
    if self.debug:
      print(f'Registering future [id = {id}]')
    self._subscribers[id] = asyncio.Future()
    await self.socket.send(json.dumps({
      'jsonrpc': '2.0',
      'id': id,
      **msg,
    }))
    try:
      r = await asyncio.wait_for(self._subscribers[id], self.timeout_secs or 2)
      if r.error is not None:
        raise r.error
      return r.result # type: ignore
    
    except asyncio.TimeoutError:
      raise DeribitError(code=-1, message='Timed Out')
