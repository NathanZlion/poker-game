from typing import Optional
from src.hand_package.domain.value_objects.action import ActionObject
from src.hand_package.infrastructure.repository.hand_repository import HandRepository
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.value_objects.hand import CreateHand
from src.hand_package.domain.value_objects.action import Action
from src.hand_package.infrastructure.services.poker_service import PokerService
from src.hand_package.presentation.schema.action import ActionModel
from src.hand_package.presentation.schema.hands import CreateHandModel


class HandService:
    def __init__(self, hand_repository: HandRepository, poker_service: PokerService):
        self.hand_repository = hand_repository
        self.poker_service = poker_service

    def create_hand(self, create_hand_model: CreateHandModel) -> Optional[Hand]:
        # convert the model into a value object
        create_hand_value_object: CreateHand = CreateHand(
            **create_hand_model.model_dump()
        )
        hand: Hand = self.poker_service.create_hand(create_hand_value_object)

        success = self.hand_repository.create_hand(hand)
        if success:
            return hand

    def perform_action(self, actionModel: ActionModel) -> ActionObject:
        action: Action = Action(**actionModel.model_dump())

        hand = self.hand_repository.get_hand(action.hand_id)

        if not hand:
            return ActionObject(success=False, message="Hand with such id doesn't exist.")

        return self.poker_service.perform_action_on_hand(action, hand)
        # success, updated_hand = self.poker_service.perform_action_on_hand(action, hand)

        # if not success:
        #     return ActionObject(success=False)

        # repository_response  = self.hand_repository.update_hand(updated_hand)

        # return ActionObject(
        #     success=repository_response,
        # )

    def get_hand(self, hand_id: str) -> Hand | None:
        return self.hand_repository.get_hand(hand_id)

    def get_hand_history(self, hand_status: Optional[bool]) -> list[Hand]:
        return self.hand_repository.get_hand_history(hand_status=hand_status)
