from fastapi import FastAPI

app = FastAPI(title="CodexVideos API", version="0.1.0")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/version")
def version():
    return {"version": "0.1.0", "service": "CodexVideos API"}


@app.post("/run/generate")
def run_generate_placeholder():
    return {"message": "TODO: trigger generate job via API"}
