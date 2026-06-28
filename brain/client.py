from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


AVAILABLE_ROOMS = {
    "astrophysics",
    "digital_art",
    "business_ideas",
    "daily_life",
    "engineering",
    "languages",
}


@dataclass
class VoxieClient:
    """Top-level client for the voxie-bestie assistant.

    Manages the active conversation room and message history.
    """

    active_room: Optional[str] = None
    history: list[dict[str, str]] = field(default_factory=list)

    def enter_room(self, room: str) -> None:
        """Set the active topic room.

        Raises ValueError for unknown rooms.
        """
        if room not in AVAILABLE_ROOMS:
            raise ValueError(
                f"Unknown room '{room}'. Available rooms: {sorted(AVAILABLE_ROOMS)}"
            )
        self.active_room = room

    def send(self, message: str) -> str:
        """Record a user message and return a placeholder response.

        Real response generation will be wired through brain/peripherals later.
        """
        if not message or not message.strip():
            raise ValueError("Message must not be empty.")
        entry = {"role": "user", "content": message, "room": self.active_room}
        self.history.append(entry)
        response = f"[{self.active_room or 'general'}] Received: {message}"
        self.history.append({"role": "assistant", "content": response, "room": self.active_room})
        return response

    def clear_history(self) -> None:
        self.history.clear()

    def leave_room(self) -> None:
        self.active_room = None
