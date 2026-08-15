from fastapi import APIRouter

# access the same milvus service instance used for registration
from app.services.registration_service import milvus_service

router = APIRouter(
    prefix="/debug",
    tags=["Debug"]
)


@router.get("/registrations")
async def registrations():
    """Return quick debug info about in-memory registered embeddings."""
    try:
        store = getattr(milvus_service.db, "_memory_store", None)
        if store is None:
            return {"count": 0, "entries": []}

        return {"count": len(store), "entries": [{"id": e[0]} for e in store]}
    except Exception as exc:
        return {"error": str(exc)}
