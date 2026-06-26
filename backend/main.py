from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import metrics
from backend.workers.data_sync import fetch_and_cache_fiscal_data
from apscheduler.schedulers.background import BackgroundScheduler
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Pull initial data point immediately on server spin up to clear out 404s
    fetch_and_cache_fiscal_data()
    
    # Run the ingestion script automatically every hour
    scheduler = BackgroundScheduler()
    scheduler.add_job(fetch_and_cache_fiscal_data, 'interval', hours=1)
    scheduler.start()
    
    yield
    scheduler.shutdown()

app = FastAPI(title="US Fiscal Dashboard API Core", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach modular endpoints router
app.include_router(metrics.router)

@app.get("/")
def read_root():
    return {"status": "online", "message": "US Fiscal Intelligence Backend Active."}
