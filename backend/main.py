from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.seed import init_db
from backend.routers import auth, leads, projects, analytics

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and seed initial data
    try:
        init_db()
    except Exception as e:
        print(f"Startup DB Seed Warning: {e}")
    yield

app = FastAPI(
    title="Rey Web Studio API",
    description="Full-stack backend API for Rey Web Studio",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(leads.router)
app.include_router(projects.router)
app.include_router(analytics.router)

# Mount Static Files at root level
app.mount("/", StaticFiles(directory=".", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
