from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Literal["user", "assistant"]
    content: str = Field(
        min_length=1,
        max_length=12000,
    )


class UserPrompt(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str = Field(
        min_length=1,
        max_length=12000,
    )

    message_history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=30,
    )

    control_mode: bool = False
