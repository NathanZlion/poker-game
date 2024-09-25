from typing import List, Optional
from psycopg2.extensions import connection
from src.hand_package.domain.entities.hand import Hand


class HandRepository:
    def __init__(self, db_connection: connection):
        self.db_Connection = db_connection

    def create_hand(self, hand: Hand) -> bool:
        with self.db_Connection.cursor() as cursor:
            try:
                cursor.execute(
                    """
                        INSERT INTO hands (
                            has_ended,
                            number_of_players,
                            small_blind_idx,
                            big_blind_idx,
                            dealer_idx,
                            stack_size,
                            big_blind_size
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
                    """,
                    (
                        hand.has_ended,
                        hand.number_of_players,
                        hand.small_blind_idx,
                        hand.big_blind_idx,
                        hand.dealer_idx,
                        hand.stack_size,
                        hand.big_blind_size,
                    ),
                )
                return True
            except:
                return False


    def get_hand(self, hand_id: str) -> Hand | None:
        with self.db_Connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT * FROM hands WHERE id = %s;
                """,
                (hand_id,),
            )

            hand = cursor.fetchone()
            if not hand:
                return None

            return Hand(
                id=hand[0],
                has_ended=hand[1],
                number_of_players=hand[2],
                small_blind_idx=hand[3],
                big_blind_idx=hand[4],
                dealer_idx=hand[5],
                stack_size=hand[6],
                big_blind_size=hand[7],
            )

    def get_hand_history(self, hand_status: Optional[bool]) -> List[Hand]:
        with self.db_Connection.cursor() as cursor:
            if hand_status is not None:
                cursor.execute(
                    """
                        SELECT * FROM hands
                        WHERE has_ended = %s;
                        ;
                    """,
                    (hand_status), # type: ignore
                )
            else:
                cursor.execute(
                    """
                        SELECT * FROM hands;
                    """
                )

            hands = cursor.fetchall()
            return [
                Hand(
                    id=hand[0],
                    has_ended=hand[1],
                    number_of_players=hand[2],
                    small_blind_idx=hand[3],
                    big_blind_idx=hand[4],
                    dealer_idx=hand[5],
                    stack_size=hand[6],
                    big_blind_size=hand[7],
                )
                for hand in hands
            ]

    def update_hand(self, hand: Hand) -> bool:
        try:
            with self.db_Connection.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE hands
                        SET has_ended = %s,
                            number_of_players = %s,
                            small_blind_idx = %s,
                            big_blind_idx = %s,
                            dealer_idx = %s,
                            stack_size = %s,
                            big_blind_size = %s
                        WHERE id = %s;
                    """,
                    (
                        hand.has_ended,
                        hand.number_of_players,
                        hand.small_blind_idx,
                        hand.big_blind_idx,
                        hand.dealer_idx,
                        hand.stack_size,
                        hand.big_blind_size,
                        hand.id,
                    ),
                )
            return True
        except:
            return False
