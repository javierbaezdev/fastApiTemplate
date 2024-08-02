from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .API.v1 import v1_router


app = FastAPI(tittle="japiCar Backend", description="japiCar Backend", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Main"])
def main():
    
    return {"message": "api is running"}


app.include_router(v1_router, prefix="/api/v1")



