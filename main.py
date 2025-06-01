from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, analytics, upload

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth")
app.include_router(analytics.router, prefix="/analytics")
app.include_router(upload.router, prefix="/data")

@app.get("/")
def read_root():
    return {"message": "InsightIQ Backend is running"}
