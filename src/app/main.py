import os
from fastapi import FastAPI, HTTPException, Request

app = FastAPI(title="Multi-Region Enterprise App")

# Uzimamo ime regije iz environment varijabli (ovo postavlja Docker/K8s)
REGION_NAME = os.getenv("AWS_REGION", "unknown-region")

# Interno stanje aplikacije (da li je zdrava ili ne)
is_healthy = True

@app.get("/")
async def root():
    return {
        "status": "success",
        "message": f"Pozdrav iz aplikacije! Trenutna regija: {REGION_NAME}"
    }

@app.get("/health")
async def health_check():
    if not is_healthy:
        raise HTTPException(status_code=500, detail="Aplikacija je u kvaru (Simulacija)")
    return {"status": "healthy", "region": REGION_NAME}

@app.post("/toggle-health")
async def toggle_health():
    """Endpoint koji koristimo za ručnu simulaciju katastrofe"""
    global is_healthy
    is_healthy = not is_healthy
    status_str = "zdrava" if is_healthy else "pokvarena"
    return {"message": f"Status aplikacije uspešno promenjen. Aplikacija je sada {status_str}."}

@app.post("/webhook")
async def alert_webhook(request: Request):
    """Ovde Alertmanager šalje request kada detektuje problem"""
    payload = await request.json()
    print(f"🚨 ALERT PRIMLJEN: {payload}")
    return {"status": "webhook_received"}
