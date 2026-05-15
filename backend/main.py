import os
import traceback
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from .database import engine, Base
from .routers import auth, teams, tasks, messages

_db_error = None
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    _db_error = str(e)

app = FastAPI(title="TaskFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(teams.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(messages.router, prefix="/api")

@app.get("/api/health")
def health():
    import os
    db_url = os.getenv("DATABASE_URL", "NOT SET")
    masked = db_url[:30] + "..." if len(db_url) > 30 else db_url
    return JSONResponse({"status": "ok" if not _db_error else "db_error", "db_url": masked, "error": _db_error})

frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    def root():
        return FileResponse(os.path.join(frontend_path, "login.html"))
