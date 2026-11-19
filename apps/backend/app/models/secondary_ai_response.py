from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator


class SecondaryAICollaborationResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str
    findings: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    additional_information: list[str] = Field(default_factory=list)


class SecondaryAIResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    content: str
    approved: bool
    issues: list[str] = Field(default_factory=list)
    suggestions: list[str] = Field(default_factory=list)
    additional_information: list[str] = Field(default_factory=list)

    verdict: Literal[
        "approved",
        "needs_revision",
        "additional_help",
    ]

    @model_validator(mode="after")
    def validate_verdict(self):
        if self.approved and self.verdict != "approved":
            raise ValueError("approved must be true when verdict is 'approved'.")

        if not self.approved and self.verdict == "approved":
            raise ValueError("approved cannot be false when verdict is 'approved'.")

        return self
