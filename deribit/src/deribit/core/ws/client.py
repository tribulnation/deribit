from typing_extensions import TypedDict, Mapping, Any, TypeVar, Generic, NotRequired, Literal
from dataclasses import dataclass
import json

from deribit.core import Client, ApiError, validator
from .multiplex_streams_rpc import MultiplexStreamsRPCSocketClient, Message

T = TypeVar('T', default=Any)

class BaseMessage(TypedDict):
  jsonrpc: str

class BaseResponse(BaseMessage):
  id: int
  testnet: bool
  usIn: int
  usOut: int
  usDiff: int

class OkResponse(BaseResponse, Generic[T]):
  result: T

class ErrorResponse(BaseResponse):
  error: ApiError

ApiResponse = OkResponse[T] | ErrorResponse

ApiResponseT: type[ApiResponse] = ApiResponse # type: ignore
validate_response = validator(ApiResponseT)

class MessageParams(TypedDict):
  channel: str
  label: NotRequired[str|None]
  data: Any

class ApiNotification(BaseMessage):
  method: Literal['subscription']
  params: MessageParams

ApiMessage = ApiNotification | ApiResponse[T]

ApiMessageT: type[ApiMessage] = ApiMessage # type: ignore
validate_message = validator(ApiMessageT)

@dataclass
class SocketClient(MultiplexStreamsRPCSocketClient[ApiResponse, Any], Client):
  
  async def req_subscription(self, channel: str):
    return await self.request('/public/subscribe', {
      'channels': [channel],
    })
  
  async def req_unsubscription(self, channel: str):
    return await self.request('/public/unsubscribe', {
      'channels': [channel],
    })
  
  async def send(self, id: int, msg: Mapping):
    data = {
      'jsonrpc': '2.0',
      'id': id,
      **msg,
    }
    await (await self.ws).send(json.dumps(data), text=True)
  
  def parse_msg(self, msg: str | bytes) -> Message[ApiResponse, Any]:
    r: ApiMessage = validate_message(msg) if self.validate else json.loads(msg)
    if 'error' in r or 'result' in r:
      return {
        'kind': 'response',
        'id': r['id'],
        'response': r
      }
    else:
      return {
        'kind': 'subscription',
        'channel': r['params']['channel'],
        'data': r['params']['data'],
      }


  async def request(self, path: str, params=None, /) -> ApiResponse:
    return await self.req({
      'jsonrpc': '2.0',
      'method': path,
      'params': params,
    })
    