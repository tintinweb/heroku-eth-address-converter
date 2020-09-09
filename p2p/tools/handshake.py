from typing import Type

from p2p.abc import MultiplexerAPI, ProtocolAPI
from p2p.handshake import Handshaker
from p2p.receipt import HandshakeReceipt


class NoopHandshaker(Handshaker[ProtocolAPI]):
    def __init__(self, protocol_class: Type[ProtocolAPI]) -> None:
        self.protocol_class = protocol_class

    async def do_handshake(self,
                           multiplexer: MultiplexerAPI,
                           protocol: ProtocolAPI) -> HandshakeReceipt:
        return HandshakeReceipt(protocol)
