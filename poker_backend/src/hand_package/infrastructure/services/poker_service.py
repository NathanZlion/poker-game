import io
from typing import List
from config.game import GameSettings
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.value_objects.action import Action, ActionObject, ActionType
from src.hand_package.domain.value_objects.hand import CreateHand
from pokerkit import Automation, NoLimitTexasHoldem, State, Mode, HandHistory


class PokerService:

    def __init__(self):
        pass

    def create_hand(self, create_hand: CreateHand) -> Hand:

        create_hand.stackSize

        state: State = NoLimitTexasHoldem.create_state(
            # Automation.BOARD_DEALING,
            # Automation.HOLE_DEALING,
            # Automation.CARD_BURNING,
            automations=(
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
            ), # type: ignore
            ante_trimming_status=True,
            raw_antes={-1: 0},
            raw_blinds_or_straddles=(1000, 2000),
            min_bet=2000,
            raw_starting_stacks=[create_hand.stackSize for _ in range(create_hand.playerCount)],
            mode=Mode.CASH_GAME,
            player_count=create_hand.playerCount
        )

        # hand_history = HandHistory.from_game_state(game, state)

        # call the repository to create a hand
        return Hand(
            has_ended=False,
            number_of_players=state.player_count,
            stack_size=GameSettings.STACK_SIZE,
            big_blind_size=GameSettings.BIG_BLIND_SIZE,
            players=[f"Player-{i+1}" for i in range(state.player_count)],
            hand_history=self.__dump_hand_history(state),
        )

    def perform_action_on_hand(self, action: Action, hand: Hand) -> ActionObject:

        if not self.__can_perform_action(action, hand):
            return ActionObject()

        hand_history = self.__load_hand_history(hand)
        state = [state for state, _ in hand_history.state_actions ][-1]

        match action.type:
            case ActionType.FOLD:
                state.fold()

            case ActionType.CHECK |  ActionType.CALL:
                state.check_or_call()

            case ActionType.BET | ActionType.RAISE | ActionType.ALLIN:
                state.complete_bet_or_raise_to(action.amount)

        updated_hand_history = self.__dump_hand_history(state)
        hand.hand_history = updated_hand_history

        return ActionObject()

    def __can_perform_action(self, action: Action, hand: Hand) -> bool:
        final_state = [
            state for state, _ in self.__load_hand_history(hand).state_actions
        ][-1]

        match action.type:
            case ActionType.FOLD:
                return final_state.can_fold()

            case ActionType.CHECK |  ActionType.CALL:
                return final_state.can_check_or_call()

            case ActionType.BET | ActionType.RAISE | ActionType.ALLIN:
                return final_state.can_complete_bet_or_raise_to(action.amount)

        return False

    def get_allowed_actions(self, hand: Hand) -> List[ActionType]:
        allowed_actions = []

        for action_type in ActionType:
            action: Action = Action(
                hand_id=hand.id, type=action_type, amount=0, description=""
            )
            if self.__can_perform_action(action, hand):
                allowed_actions.append(action_type)

        return allowed_actions

    def __dump_hand_history(self, state: State) -> str:
        game : NoLimitTexasHoldem = NoLimitTexasHoldem(
            # Automation.BOARD_DEALING,
            # Automation.BLIND_OR_STRADDLE_POSTING,
            # Automation.HOLE_DEALING,
            automations=(
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CARD_BURNING
            ),  #type: ignore
            ante_trimming_status=True,
            raw_antes={-1: 0},
            raw_blinds_or_straddles=(1000, 2000),
            min_bet=2000,
            mode=Mode.CASH_GAME
        )

        hand_history = HandHistory.from_game_state(game, state)
        buffer = io.BytesIO()
        hand_history.dump(buffer)
        game_str = buffer.getvalue().decode('utf-8')

        return game_str

    def __get_history_from_hand_history(self, hand_history: HandHistory) -> str:
        buffer = io.BytesIO()
        hand_history.dump(buffer)
        game_str = buffer.getvalue().decode('utf-8')

        return game_str

    def __load_hand_history(self, hand: Hand) -> HandHistory:
        return HandHistory.load(io.BytesIO(bytes(hand.hand_history, encoding="utf-8")))
