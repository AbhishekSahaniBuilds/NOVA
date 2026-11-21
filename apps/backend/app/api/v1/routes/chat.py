import logging

from fastapi import APIRouter, HTTPException, Request, status

from app.agents.chat_agent import process_chat
from app.models.prompt import UserPrompt

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/")
async def chat(
    prompt: UserPrompt,
    request: Request,
):
    try:
        response = await process_chat(
            main_ai_client=request.app.state.groq_client,
            content=prompt.content,
            message_history=prompt.message_history,
            control_mode=prompt.control_mode,
            tool_approval=prompt.tool_approval,
        )

        if not response.get("success"):
            logger.error("Chat processing failed.")

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Unable to process your message. Check the server logs for details.",
            )

        return response

    except HTTPException:
        raise

    except Exception:
        logger.exception("Unexpected error in chat endpoint.")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected server error occurred.",
        )
