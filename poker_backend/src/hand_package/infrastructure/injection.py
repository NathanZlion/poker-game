# Dependency Injection for the Infrastructure Layer

from fastapi import Depends
from src.hand_package.infrastructure.repository.hand_repository import HandRepository
from src.hand_package.infrastructure.services.hand_service import HandService
from src.core.database.database import getDatabaseConnection
from psycopg2.extensions import connection


def get_hand_repository(
    db_connection: connection = Depends(getDatabaseConnection),
) -> HandRepository:
    return HandRepository(db_connection=db_connection)


def get_hand_service(
    hand_repository: HandRepository = Depends(get_hand_repository),
) -> HandService:
    return HandService(hand_repository=hand_repository)
