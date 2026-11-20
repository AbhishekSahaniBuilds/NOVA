from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class MainAIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
