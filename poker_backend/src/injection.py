from functools import cache
from fastapi import Depends
from psycopg2.extensions import connection
from src.hand_package.domain.services.poker_service import PokerService
from src.hand_package.infrastructure.repository.hand_repository import HandRepository
from src.hand_package.domain.services.hand_service import HandService
from src.hand_package.domain.services.hand_service import HandService
from src.hand_package.domain.services.poker_service import PokerService
from src.core.database.database import getDatabaseConnection
from src.hand_package.infrastructure.repository.hand_repository import HandRepository


@cache
def get_poker_service() -> PokerService:
    return PokerService()


@cache
def get_hand_repository(
    db_connection: connection = Depends(getDatabaseConnection),
) -> HandRepository:
    return HandRepository(db_connection=db_connection)


@cache
def get_hand_service(
    hand_repository: HandRepository = Depends(get_hand_repository),
    poker_service: PokerService = Depends(get_poker_service),
) -> HandService:
    return HandService(
        hand_repository=hand_repository,
        poker_service=poker_service,
    )
