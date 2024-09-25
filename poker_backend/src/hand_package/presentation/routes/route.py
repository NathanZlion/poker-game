from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.infrastructure.injection import get_hand_service
from src.hand_package.infrastructure.services.hand_service import HandService
from src.hand_package.presentation.schema.action import ActionModel, ActionResponse
from src.hand_package.presentation.schema.hands import (
    CreateHandModel,
    HandHistoryResponse,
    HandResponse,
)


hand_router = APIRouter()


@hand_router.post(
    "/hands",
    response_model=HandResponse,
    response_description="The hand that was created.",
)
def new_hand(
    hand_data: CreateHandModel,
    hand_service: HandService = Depends(get_hand_service),
):
    """Create a new hand, and start the game."""

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

    return HandResponse(
        id=hand.id,
        has_ended=hand.has_ended,
        small_blind_idx=hand.small_blind_idx,
        big_blind_idx=hand.big_blind_idx,
        dealer_idx=hand.dealer_idx,
        number_of_players=hand.number_of_players,
        stack_size=hand.stack_size
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
    action_response: ActionResponse = ActionResponse(
        success=result.success,
        message=result.message,
        next_actor=result.next_actor,
        current_actor=result.current_actor,
        dealt_cards=result.dealt_cards,
        game_has_ended=result.game_has_ended,

    )

    # the action failed, or not allowed
    if not action_response.success:
        raise HTTPException(status_code=400, detail=action_response.message)

    return action_response
