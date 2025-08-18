import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",   # path to your FastAPI app
        host="0.0.0.0",   # allow access from outside (Docker / Render)
        port=8000,
        reload=True,      # auto-reload during development
        workers=1         # 1 worker recommended for async endpoints on Python 3.12
    )
