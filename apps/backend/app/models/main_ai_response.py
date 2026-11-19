from typing import Any

from pydantic import BaseModel, ConfigDict, Field, model_validator


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1)
    arguments: dict[str, Any] = Field(default_factory=dict)


class SecondaryAITask(BaseModel):
    model_config = ConfigDict(extra="forbid")

    needed: bool = False
    task: str = ""
    purpose: str = ""

    @model_validator(mode="after")
    def validate_task(self):
        if self.needed and not self.task.strip():
            raise ValueError(
                "A task must be provided when SecondaryAI collaboration is needed."
            )

        return self


class MainAIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str
    tool_calls: list[ToolCall] = Field(default_factory=list)
    secondary_task: SecondaryAITask = Field(default_factory=SecondaryAITask)
    review_required: bool = False
