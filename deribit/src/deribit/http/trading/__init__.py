# deribit/http/trading/__init__.py

from dataclasses import dataclass, field
from deribit.http.client import AuthedClient
from .buy import Buy

@dataclass
class Trading(Buy):
  client: AuthedClient = field(default_factory=AuthedClient.oauth2)