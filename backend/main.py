from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import metrics [cite: 92, 93, 94]

app = FastAPI(title="US Fiscal Dashboard API") [cite: 95]

# Allow your frontend to communicate with this backend securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to your actual frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
) [cite: 96, 97, 98, 99, 100, 101, 102, 103]

# Include the modular routers
app.include_router(metrics.router) [cite: 104, 105]

@app.get("/")
def read_root():
    return {"message": "US Fiscal Intelligence Backend Active."} [cite: 106, 107, 108]
