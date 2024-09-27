from typing import List, Optional
from psycopg2.extensions import connection
from src.hand_package.domain.entities.hand import Hand


class HandRepository:

    def __init__(self, db_connection: connection):
        self.db_Connection = db_connection

    def create_hand(self, hand: Hand) -> Hand:

        with self.db_Connection.cursor() as cursor:
            cursor.execute(
                """
                    INSERT INTO hands (
                        game_has_ended,
                        hand_history
                    )
                    VALUES (%s, %s) RETURNING id;
                """,
                (
                    hand.game_has_ended,
                    hand.hand_history
                ),
            )

            self.db_Connection.commit()
            created_hand = cursor.fetchone()

            if created_hand is None:
                raise ValueError("Hand was not created.")

            return Hand(
                id=created_hand[0],
                game_has_ended=hand.game_has_ended,
                hand_history=hand.hand_history,
            )

    def get_hand(self, hand_id: str) -> Hand | None:
        with self.db_Connection.cursor() as cursor:
            cursor.execute(
                """
                    SELECT * FROM hands WHERE id = %s;
                """,
                (hand_id,),
            )

            fetched_hand = cursor.fetchone()
            if not fetched_hand:
                return None

            return Hand(
                id=fetched_hand[0],
                game_has_ended=fetched_hand[1],
                hand_history=fetched_hand[2],
            )

    def get_hand_history(self, hand_status: Optional[bool]) -> List[Hand]:
        with self.db_Connection.cursor() as cursor:
            if hand_status is not None:
                cursor.execute(
                    """
                        SELECT * FROM hands
                        WHERE has_ended = %s;
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
                Hand(id=hand[0], game_has_ended=hand[1], hand_history=hand[2])
                for hand in hands
            ]

    def update_hand(self, hand: Hand) -> Hand:
        try:
            with self.db_Connection.cursor() as cursor:
                cursor.execute(
                    """
                        UPDATE hands
                        SET game_has_ended = %s,
                            hand_history = %s
                        WHERE id = %s;
                    """,
                    (
                        hand.game_has_ended,
                        hand.hand_history,
                        hand.id,
                    ),
                )
            self.db_Connection.commit()
            return hand
        except:
            raise ValueError("Hand was not updated.")
