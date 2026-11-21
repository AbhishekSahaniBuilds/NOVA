from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from app.models.main_ai_response import ToolCall


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: Literal["user", "assistant"]
    content: str = Field(
        min_length=1,
        max_length=12000,
    )

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message content cannot be blank.")
        return value


class ToolApproval(BaseModel):
    model_config = ConfigDict(extra="forbid")

    decision: Literal["approved", "denied"]
    tool_calls: list[ToolCall] = Field(min_length=1)


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

    tool_approval: ToolApproval | None = None

    @field_validator("content")
    @classmethod
    def content_must_not_be_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Message content cannot be blank.")
        return value
