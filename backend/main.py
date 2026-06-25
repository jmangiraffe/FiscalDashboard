from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import metrics

app = FastAPI(title="US Fiscal Dashboard API")

# Allow your frontend to communicate with this backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to your actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the modular routers
app.include_router(metrics.router)

@app.get("/")
def read_root():
    return {"message": "US Fiscal Intelligence Backend Active."}
