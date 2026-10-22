# engine/message.py
from dataclasses import dataclass, field
from typing import Any, Dict
import time
import uuid

@dataclass
class Message:
    sender: str
    receiver: str
    content: Any
    msg_type: str = "text"
    msg_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __str__(self):
        return f"[{self.sender} -> {self.receiver}] {self.msg_type}: {self.content}"