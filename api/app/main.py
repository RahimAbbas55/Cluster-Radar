from fastapi import FastAPI
from .routes import feeds

app = FastAPI(title="Cluster-Radar API")
app.include_router(feeds.router)

@app.get("/health")
def health():
    # used by k8s liveness/readiness probes later
    return {"status": "ok"}