from typing import List, Optional
from src.hand_package.domain.value_objects.action import ActionObject
from src.hand_package.infrastructure.repository.hand_repository import HandRepository
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.value_objects.hand import CreateHand
from src.hand_package.domain.value_objects.action import Action
from src.hand_package.domain.services.poker_service import PokerService
from src.hand_package.presentation.schema.action import ActionModel
from src.hand_package.presentation.schema.hands import CreateHandModel, HandHistoryResponse, HandResponse
from src.hand_package.presentation.schema.action import ActionResponse


class HandService:

    def __init__(self, hand_repository: HandRepository, poker_service: PokerService):
        self.hand_repository = hand_repository
        self.poker_service = poker_service

    def create_hand(self, create_hand_model: CreateHandModel) -> HandResponse:
        # convert the model into a value object
        create_hand_value_object: CreateHand = CreateHand(
            **create_hand_model.model_dump()
        )

        hand: Hand = self.poker_service.create_hand(create_hand_value_object)
        hand = self.hand_repository.create_hand(hand)

        allowed_actions, logs, game_has_ended, total_pot_size = self.poker_service.analyse_hand(hand)

        return HandResponse(
            id=hand.id,
            message="Hand created successfully.",
            allowed_actions=allowed_actions,
            game_has_ended=game_has_ended,
            logs=logs,
            pot_amount=total_pot_size,
        )

    def perform_action(self, hand_id: str, actionModel: ActionModel) -> ActionResponse:
        action: Action = Action(**actionModel.model_dump())
        hand = self.hand_repository.get_hand(hand_id)

        # No such action
        if not hand:
            return ActionResponse(
                id="-1",
                success=False,
                message="Hand with such id doesn't exist.",
                logs=[],
                allowed_actions=[],
                game_has_ended=False,
                pot_amount=-1,
            )

        action_response, updated_hand = self.poker_service.perform_action_on_hand(action, hand)
        _, _, _, _ = self.poker_service.analyse_hand(updated_hand)

        # action cannot be performed
        if not action_response.success:
            return action_response

        self.hand_repository.update_hand(updated_hand)

        return action_response

    def get_hand(self, hand_id: str) -> Hand | None:
        return self.hand_repository.get_hand(hand_id)

    def get_hand_history(
        self, completed: Optional[bool] = True
    ) -> list[HandHistoryResponse]:
        hands : List[Hand] = self.hand_repository.get_hand_history(hand_status=completed)

        handhistories : List[HandHistoryResponse] = [
            self.poker_service.get_formatted_hand_history(hand)
            for hand in hands
        ]

        return handhistories
