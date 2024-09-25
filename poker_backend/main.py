from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.models import Healthy
from src.hand_package.presentation.routes.route import hand_router
from config.settings import allowed_origins, version

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"/api/v{version}")
async def root():
    return Healthy()


app.include_router(
    hand_router,
    prefix=f"/api/v{version}",
)
