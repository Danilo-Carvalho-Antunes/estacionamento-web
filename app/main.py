from fastapi import FastAPI

app = FastAPI(title="Estacionamento API")


@app.get("/health")
def health():
    return {"status": "ok"}
