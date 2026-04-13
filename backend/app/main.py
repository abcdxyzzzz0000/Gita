from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import traceback

from app.config import get_settings
from app.routes import auth, content, health, rag, oauth, bookmarks, profile, search, daily_wisdom, audio, life_guidance, progress, account, chat
from app.routes import settings as settings_routes

app_settings = get_settings()

app = FastAPI(
    title=app_settings.app_name,
    version="1.0.0",
    description="REST API for Bhagavad Gita learning application with RAG-powered explanations",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=app_settings.api_prefix)
app.include_router(auth.router, prefix=app_settings.api_prefix)
app.include_router(content.router, prefix=app_settings.api_prefix)
app.include_router(rag.router, prefix=app_settings.api_prefix)
app.include_router(oauth.router, prefix=app_settings.api_prefix)
app.include_router(bookmarks.router, prefix=app_settings.api_prefix)
app.include_router(profile.router, prefix=app_settings.api_prefix)
app.include_router(search.router, prefix=app_settings.api_prefix)
app.include_router(daily_wisdom.router, prefix=app_settings.api_prefix)
app.include_router(settings_routes.router, prefix=app_settings.api_prefix)
app.include_router(audio.router, prefix=app_settings.api_prefix)
app.include_router(life_guidance.router, prefix=app_settings.api_prefix)
app.include_router(progress.router, prefix=app_settings.api_prefix)
app.include_router(account.router, prefix=app_settings.api_prefix)
app.include_router(chat.router, prefix=app_settings.api_prefix)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    traceback.print_exc()
    return JSONResponse(status_code=500, content={"detail": str(exc)})


@app.get("/")
async def root():
    return {"message": "Bhagavad Gita Learning API", "docs": "/api/docs"}
