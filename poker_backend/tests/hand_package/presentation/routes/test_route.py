from typing import List, Optional

from fastapi.testclient import TestClient

from src.hand_package.domain.entities.hand import Hand
from src.hand_package.presentation.schema.action import (
    ActionModel,
    ActionResponse,
    ActionType,
)
from src.hand_package.presentation.schema.hands import (
    CreateHandModel,
    HandHistoryResponse,
)
from src.injection import get_hand_service
from src.main import app


testing_client = TestClient(app)

MockHandHistoryResponse = [
    {
        "id": "399ef5bd-d75d-406f-8bff-477ab502e1a2",
        "stack": 10000,
        "dealer": "Player 6",
        "small_blind_player": "Player 1",
        "big_blind_player": "Player 2",
        "actions": "f:f:f:f:x:x Jc6c9h b20:x Td b20:x 5h b20:x",
        "hands": {
            "Player 1": "Th9s",
            "Player 2": "2s7c",
            "Player 3": "8cAs",
            "Player 4": "Ad3c",
            "Player 5": "Qc6h",
            "Player 6": "Tc4c",
        },
        "winnings": {
            "Player 1": 100,
            "Player 2": -100,
            "Player 3": 0,
            "Player 4": 0,
            "Player 5": 0,
            "Player 6": 0,
        },
    }
]


class MockHandService:
    def create_hand(self, _: CreateHandModel):
        return {
            "id": "1",
            "allowed_actions": ["FOLD", "CHECK", "BET"],
            "message": "Player 1, it's your turn",
            "logs": ["Player 1, it's your turn"],
            "game_has_ended": False,
            "pot_amount": 0,
            "minimum_bet_or_raise_amount": 10,
        }

    def get_hand_history(
        self, _: Optional[bool] = True
    ) -> list[HandHistoryResponse]:
        _: List[Hand] = []
        handhistories: List[HandHistoryResponse] = [
            HandHistoryResponse(
                id=a["id"],
                stack=a["stack"],
                dealer=a["dealer"],
                small_blind_player=a["small_blind_player"],
                big_blind_player=a["big_blind_player"],
                actions=a["actions"],
                hands=a["hands"],
                winnings=a["winnings"],
            )
            for a in MockHandHistoryResponse
        ]

        return handhistories


def override_get_hand_service():
    return MockHandService()


# override the get_hand_service dependency
app.dependency_overrides[get_hand_service] = override_get_hand_service


def test_create_hand_success():
    response = testing_client.post(
        "/api/v1/new_hand",
        json={
            "player_count": 6,
            "stack_size": 1000,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "allowed_actions": ["FOLD", "CHECK", "BET"],
        "message": "Player 1, it's your turn",
        "logs": ["Player 1, it's your turn"],
        "game_has_ended": False,
        "pot_amount": 0,
        "minimum_bet_or_raise_amount": 10,
    }


def test_create_hand_fail():
    response = testing_client.post(
        "/api/v1/new_hand", json={"player_count": 6, "stack_size": "abcd"}
    )
    assert response.status_code == 422  # unprocessable entity error


def test_get_hand_history_success():
    response = testing_client.get("/api/v1/hands")
    assert response.status_code == 200
    assert response.json() == MockHandHistoryResponse


class MockHandServiceEmptyHandHistory:
    def get_hand_history(
        self, _: Optional[bool] = True
    ) -> list[HandHistoryResponse]:
        return []


def override_get_hand_service_empty_hand_history():
    return MockHandServiceEmptyHandHistory()


def test_get_hand_history_failure():
    app.dependency_overrides[get_hand_service] = (
        override_get_hand_service_empty_hand_history
    )
    response = testing_client.get("/api/v1/hands")
    assert response.status_code == 404


class MockHandServicePerformActionSuccess:
    def perform_action(
        self, _handId: str, _actionModel: ActionModel
    ) -> ActionResponse:
        del _handId
        del _actionModel

        return ActionResponse(
            id="1",
            success=True,
            message="Player 2, it's your turn",
            logs=["Player 1, it's your turn", "Player 2, it's your turn"],
            allowed_actions=[ActionType.FOLD, ActionType.ALLIN],
            game_has_ended=False,
            pot_amount=10,
            minimum_bet_or_raise_amount=20,
        )


def override_get_hand_service_perform_action_success():
    return MockHandServicePerformActionSuccess()


def test_perform_action_success():
    """Test the perform action route, successfull action"""
    app.dependency_overrides[get_hand_service] = (
        override_get_hand_service_perform_action_success
    )
    response = testing_client.post(
        "/api/v1/hands/1/actions",
        json={
            "type": "FOLD",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": "1",
        "success": True,
        "message": "Player 2, it's your turn",
        "logs": ["Player 1, it's your turn", "Player 2, it's your turn"],
        "allowed_actions": ["FOLD", "ALL_IN"],
        "game_has_ended": False,
        "pot_amount": 10,
        "minimum_bet_or_raise_amount": 20,
    }


class MockHandServicePerformActionHandNotFound:
    def perform_action(
        self, _handId: str, _actionModel: ActionModel
    ) -> ActionResponse:
        del _handId
        del _actionModel

        return ActionResponse(
            id="-1",
            success=False,
            message="Hand with such id doesn't exist.",
            logs=[],
            allowed_actions=[],
            game_has_ended=False,
            pot_amount=-1,
            minimum_bet_or_raise_amount=-1,
        )


def override_get_hand_service_perform_action_hand_not_found():
    return MockHandServicePerformActionHandNotFound()


def test_perform_action_fail_hand_not_found():
    """Test the perform action route, hand not found"""
    app.dependency_overrides[get_hand_service] = (
        override_get_hand_service_perform_action_hand_not_found
    )
    response = testing_client.post(
        "/api/v1/hands/1/actions",
        json={
            "type": "FOLD",
        },
    )

    assert response.status_code == 400
    assert (
        response.json()["detail"]["message"]
        == "Hand with such id doesn't exist."
    )


def test_performance_action_fail_invalid_entity():
    """Test the perform action route, invalid action"""
    response = testing_client.post(
        "/api/v1/hands/1/actions",
        json={
            "type": "INVALID_ACTION_TYPE",
        },
    )
    assert response.status_code == 422
