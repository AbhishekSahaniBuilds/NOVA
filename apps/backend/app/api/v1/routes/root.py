from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return Response(status_code=204)


@router.get("/")
async def root():
    return {
        "name": "NOVA",
        "full_name": "Neural Omni Vector Assistant",
        "description": "Backend API for NOVA",
        "version": "0.1.0",
        "status": "running",
        "docs": "/docs",
        "health": "/v1/health",
    }
