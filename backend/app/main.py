from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import router as auth_router

app = FastAPI(title="Face Authentication System")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the real authentication routes
app.include_router(auth_router)

@app.get("/debug/registrations")
async def debug_registrations():
    # Return count of registrations for the dashboard's initial check
    try:
        from app.database.milvus_client import milvus_client
        if hasattr(milvus_client, "_memory_store"):
            return {"count": len(milvus_client._memory_store)}
        else:
            return {"count": 1} # Mock if using real Milvus DB
    except Exception:
        return {"count": 0}
