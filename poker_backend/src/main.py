from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.database.create_tables import create_tables
from src.core.database.database import getDatabaseConnection
from src.models import Healthy
from src.hand_package.presentation.routes.route import hand_router
from src.config.settings import allowed_origins, version
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(_: FastAPI):
    create_tables()
    yield
    conn = getDatabaseConnection()
    if conn:
        conn.close()
        print("--> Database connection closed on app shutdown.")

app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(f"/api/v{version}")
async def check_health():
    return Healthy()


app.include_router(
    hand_router,
    prefix=f"/api/v{version}",
)

