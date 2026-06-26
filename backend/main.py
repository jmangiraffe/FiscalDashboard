import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import metrics
from backend.workers.data_sync import fetch_and_cache_fiscal_data
from apscheduler.schedulers.background import BackgroundScheduler

@asynccontextmanager
async def lifespan(app: FastAPI):
    fetch_and_cache_fiscal_data()

    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_cache_fiscal_data, "interval", hours=1)
    scheduler.start()

    yield
    scheduler.shutdown()

app = FastAPI(title="US Fiscal Dashboard API", lifespan=lifespan)

ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

app.include_router(metrics.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "US Fiscal Intelligence Backend Active."}
