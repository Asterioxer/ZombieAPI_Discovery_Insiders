"""
ZombieGuard — Mock Vulnerable Banking API (Demo Target)
Boot up: python mock_vulnerable_bank.py
Runs on: http://localhost:8001
Spec URL: http://localhost:8001/openapi.json
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

app = FastAPI(
    title="UnionBank Legacy Core API",
    description="Mock target API containing severe Zombie API endpoints and exposed debug consoles for ZombieGuard demonstration.",
    version="1.4.2",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ═══════════════════════════════════════════════════════════════
# 1. ACTIVE SECURE ENDPOINTS (Should scan as LOW risk)
# ═══════════════════════════════════════════════════════════════
@app.get("/api/v2/accounts/{id}/balance", summary="Retrieve account balance", tags=["Accounts"])
def get_balance(id: str):
    """Secure balance check. Auth: Bearer token required."""
    return {"account_id": id, "balance": 45209.87, "currency": "INR"}

@app.post("/api/v2/payments/initiate", summary="Initiate fund transfer", tags=["Payments"])
def initiate_payment():
    """Secure NEFT/IMPS transfer. Auth: Bearer token required."""
    return {"transfer_id": "TXN90284091", "status": "SUCCESS"}


# ═══════════════════════════════════════════════════════════════
# 2. ZOMBIE APIS (Stale, deprecrated, unauthenticated)
# ═══════════════════════════════════════════════════════════════
@app.get("/api/v1/accounts/balance", summary="Legacy balance check", tags=["Legacy Core"])
def legacy_balance():
    """Deprecated legacy endpoint left running in production. Auth: None (Public)."""
    return {"message": "WARNING: Legacy endpoint.", "balance": 45209.87}

@app.post("/api/v1/payment/test", summary="Legacy payment testing interface", tags=["Legacy Core"])
def legacy_payment_test():
    """Stale testing interface left exposed. Auth: None (Public)."""
    return {"message": "Test transaction initiated", "sandbox_mode": True}


# ═══════════════════════════════════════════════════════════════
# 3. CRITICAL SHADOW/VULNERABLE APIS (Triggers CVE rules in Scorer)
# ═══════════════════════════════════════════════════════════════
@app.get("/api/internal/debug/sql", summary="Internal debug SQL console", tags=["Debug"])
def debug_sql():
    """
    CRITICAL VULNERABILITY! Exposed SQL Console.
    Matches CVE-2023-1234 (debug) and CVE-2021-9012 (sql) patterns!
    """
    return {"status": "CONNECTED", "database": "core_banking_prod"}

@app.post("/api/v1/admin/users/reset", summary="Legacy admin reset bypass", tags=["Legacy Core"])
def admin_reset():
    """
    HIGH VULNERABILITY! Legacy admin password reset without authentication.
    Matches CVE-2022-5678 (admin) and CVE-2020-0002 (v1) legacy patterns!
    """
    return {"message": "Admin bypass console active", "warning": "Unauthenticated reset enabled"}


if __name__ == "__main__":
    print("=" * 60)
    print(" 🏦 UnionBank Legacy Core API — Mock Demo Target Booted")
    print(" Runs on: http://localhost:8001")
    print(" Spec    : http://localhost:8001/openapi.json")
    print(" Docs    : http://localhost:8001/docs")
    print("=" * 60)
    uvicorn.run(app, host="0.0.0.0", port=8001)
