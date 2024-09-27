from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from injection import get_hand_service
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.services.hand_service import HandService
from src.hand_package.presentation.schema.action import ActionModel, ActionResponse
from src.hand_package.presentation.schema.hands import (
    CreateHandModel,
    HandHistoryResponse,
    HandResponse,
)


hand_router = APIRouter()


@hand_router.post(
    "/new_hand",
    response_model=HandResponse,
    response_description="The hand that was created.",
)
def create_hand(
    hand_data: CreateHandModel,
    hand_service: HandService = Depends(get_hand_service),
):
    """Create a new hand, and start the game. 

    Returns a HandResponse
    """
    create_hand_response = hand_service.create_hand(hand_data)
    return create_hand_response


@hand_router.get(
    "hands/{hand_id}",
    response_model=HandResponse,
)
def get_hand_by_id(
    hand_id: str,
    hand_service: HandService = Depends(get_hand_service),
):
    """Get's hand history, all hands that have ended."""

    hand = hand_service.get_hand(hand_id=hand_id)

    # hand with such id does not exist
    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found.")

    return HandResponse(  # type: ignore
        # id=hand.id,
        # has_ended=hand.has_ended,
    )


@hand_router.get("hands", response_model=HandHistoryResponse)
def get_hand_history(
    completed: bool = True,
    hand_service: HandService = Depends(get_hand_service),
):
    """Get's hand history, all hands that have ended."""

    hands: List[Hand] = hand_service.get_hand_history(
        hand_status=completed
    )

    if hands:
        return hands

    raise HTTPException(status_code=404, detail="No hands found.")


@hand_router.post(
    "hands/{hand_id}/actions",
    response_model=ActionResponse,
    response_description="The result of the action performed.",
)
def perform_action(
    action: ActionModel,
    hand_service: HandService = Depends(get_hand_service),
) -> Optional[ActionResponse]:
    """Perform an action on the hand."""

    result = hand_service.perform_action(action)
    action_response: ActionResponse = ActionResponse()  # type: ignore

    # the action failed, or not allowed
    if not action_response.success:
        raise HTTPException(status_code=400, detail=action_response.message)

    return action_response
