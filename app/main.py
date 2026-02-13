import zoneinfo
from datetime import datetime
import time
from fastapi import FastAPI, Request, Depends, HTTPException, status
from .db import SessionDep, create_all_tables
from .routers import customers, transactions, invoices, plans
from sqlmodel import select
from typing import Annotated
from fastapi.security import HTTPBasic, HTTPBasicCredentials

app = FastAPI(lifespan=create_all_tables)

app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)

@app.middleware("http")
async def log_requests_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"Request: {request.url} completed in time: {process_time:.4f} seconds")
    response.headers["X-Process-Time"] = str(process_time)
    return response

security = HTTPBasic()


@app.get("/")
async def root(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    print(credentials)
    if credentials.username == "admin" and credentials.password == "admin":
        return {"message": "Hola, Luis!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


country_timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "AR": "America/Argentina/Buenos_Aires",
    "BR": "America/Sao_Paulo",
    "PE": "America/Lima",
}


@app.get("/time/{iso_code}")
async def get_time_by_code(iso_code: str):
    iso = iso_code.upper()
    timezone_str = country_timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone_str)
    return {"time": datetime.now(tz)}
