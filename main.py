import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.routes import router

load_dotenv()

app = FastAPI(title="FlowGenie")
app.include_router(router)

frontend_dir = Path(__file__).parent / "frontend"
app.mount("/static", StaticFiles(directory=str(frontend_dir)), name="static")


@app.get("/")
def serve_frontend() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")


@app.get("/index.html")
def serve_index_html() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")


@app.get("/login")
def serve_login() -> FileResponse:
    return FileResponse(frontend_dir / "login.html")


@app.get("/login.html")
def serve_login_html() -> FileResponse:
    return FileResponse(frontend_dir / "login.html")


@app.get("/signup")
def serve_signup() -> FileResponse:
    return FileResponse(frontend_dir / "login.html")


@app.get("/signup.html")
def serve_signup_html() -> FileResponse:
    return FileResponse(frontend_dir / "login.html")


@app.get("/health")
def healthcheck() -> dict:
    return {"status": "ok"}
