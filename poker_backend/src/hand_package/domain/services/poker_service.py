import io
from typing import List, Tuple
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.value_objects.action import Action, ActionType
from src.hand_package.domain.value_objects.hand import CreateHand
from pokerkit import Automation, NoLimitTexasHoldem, State, Mode, HandHistory

from src.hand_package.presentation.schema.action import ActionResponse
from src.hand_package.presentation.schema.hands import HandHistoryResponse
from copy import deepcopy


class PokerService:
    def create_hand(self, create_hand: CreateHand) -> Hand:
        create_hand.stack_size

        state: State = NoLimitTexasHoldem.create_state(
            automations=(
                Automation.BOARD_DEALING,
                Automation.CARD_BURNING,
                Automation.HOLE_DEALING,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
            ),  # type: ignore
            ante_trimming_status=True,
            raw_antes={-1: 0},
            raw_blinds_or_straddles=(20, 40),
            min_bet=20,
            raw_starting_stacks=[
                create_hand.stack_size for _ in range(create_hand.player_count)
            ],
            mode=Mode.CASH_GAME,
            player_count=create_hand.player_count,
        )

        # call the repository to create a hand
        return Hand(
            game_has_ended=False,
            hand_history=self.__dump_hand_history(state),
        )

    def perform_action_on_hand(
        self, action: Action, hand: Hand
    ) -> Tuple[ActionResponse, Hand]:
        (
            allowed_actions,
            logs,
            game_has_ended,
            total_pot_size,
            minimum_bet_or_raise_amount,
        ) = self.analyse_hand(hand)
        hand_history = self.__load_hand_history(hand)

        final_state = [state for state, _ in hand_history.state_actions][-1]

        if game_has_ended:
            return (
                ActionResponse(
                    success=False,
                    message="Game has ended.",
                    allowed_actions=[],
                    game_has_ended=game_has_ended,
                    logs=logs,
                    pot_amount=total_pot_size,
                    minimum_bet_or_raise_amount=minimum_bet_or_raise_amount,
                ),
                hand,
            )

        # check if the action can be performed
        action_allowed, message = self.__can_perform_action(action.type, final_state)
        if not action_allowed:
            return (
                ActionResponse(
                    id=hand.id,
                    success=False,
                    message=message,
                    allowed_actions=allowed_actions,
                    game_has_ended=game_has_ended,
                    logs=logs,
                    pot_amount=total_pot_size,
                    minimum_bet_or_raise_amount=minimum_bet_or_raise_amount,
                ),
                hand,
            )

        # validate action and perform
        match action.type:
            case ActionType.FOLD:
                final_state.fold()

            case ActionType.CHECK:
                final_state.check_or_call()

            case ActionType.CALL:
                final_state.check_or_call()

            case ActionType.BET:
                if not final_state.can_complete_bet_or_raise_to(action.amount):
                    return (
                        ActionResponse(
                            id=hand.id,
                            success=False,
                            message="Cannot Bet. Amount is less than the minimum bet amount.",
                            allowed_actions=allowed_actions,
                            game_has_ended=game_has_ended,
                            logs=logs,
                            pot_amount=total_pot_size,
                            minimum_bet_or_raise_amount=minimum_bet_or_raise_amount,
                        ),
                        hand,
                    )

                final_state.complete_bet_or_raise_to(action.amount)

            case ActionType.RAISE:
                if not final_state.can_complete_bet_or_raise_to(action.amount):
                    return (
                        ActionResponse(
                            id=hand.id,
                            success=False,
                            message="Cannot raise. Amount is less than the minimum raise amount.",
                            allowed_actions=allowed_actions,
                            game_has_ended=game_has_ended,
                            logs=logs,
                            pot_amount=total_pot_size,
                            minimum_bet_or_raise_amount=final_state.min_completion_betting_or_raising_to_amount
                            or -1,
                        ),
                        hand,
                    )

                final_state.complete_bet_or_raise_to(action.amount)

            case ActionType.ALLIN:
                final_state.complete_bet_or_raise_to(
                    final_state.stacks[final_state.actor_index or 0]
                )

        updated_hand_history = self.__dump_hand_history(final_state)
        hand.hand_history = updated_hand_history
        (
            allowed_actions,
            logs,
            game_has_ended,
            total_pot_size,
            minimum_bet_or_raise_amount,
        ) = self.analyse_hand(hand)
        hand.game_has_ended = game_has_ended

        if game_has_ended:
            while final_state.status and final_state.can_show_or_muck_hole_cards():
                final_state.show_or_muck_hole_cards()

        updated_hand_history = self.__dump_hand_history(final_state)
        hand.hand_history = updated_hand_history
        (
            allowed_actions,
            logs,
            game_has_ended,
            total_pot_size,
            minimum_bet_or_raise_amount,
        ) = self.analyse_hand(hand)

        hand.game_has_ended = game_has_ended

        hand_history = self.__load_hand_history(hand)
        final_state = [state for state, _ in hand_history.state_actions][-1]
        if final_state.can_deal_board():
            final_state.deal_board()

        updated_hand_history = self.__dump_hand_history(final_state)
        hand.hand_history = updated_hand_history
        (
            allowed_actions,
            logs,
            game_has_ended,
            total_pot_size,
            minimum_bet_or_raise_amount,
        ) = self.analyse_hand(hand)
        hand.game_has_ended = game_has_ended

        return (
            ActionResponse(
                id=hand.id,
                success=True,
                message="Action performed successfully.",
                allowed_actions=allowed_actions,
                game_has_ended=game_has_ended,
                logs=logs,
                pot_amount=total_pot_size,
                minimum_bet_or_raise_amount=final_state.min_completion_betting_or_raising_to_amount
                or -1,
            ),
            hand,
        )

    def analyse_hand(
        self, hand: Hand
    ) -> Tuple[List[ActionType], List[str], bool, int, int]:
        """Analyse Hand

        returns : allowed_actions, logs, game_has_ended, total_pot_size, minimum_bet
        """
        logs = []
        hand_history = self.__load_hand_history(hand)
        players = hand_history.players
        states: List[State] = []

        for state in hand_history:
            states.append(deepcopy(state))  # Deep copy of each state

        actions = hand_history.actions
        # [action for _, action in hand_history.state_actions]
        player_count = len(players)  # type: ignore

        # log of the hole dealing
        state_after_hole_dealing = states[player_count]

        for index, action in enumerate(actions[:player_count]):
            logs.append(f"Player {index + 1} is dealt {action.split()[3]}")

        # ----
        logs.append("---")

        dealer_index = -1
        dealer = players[dealer_index]  # type: ignore
        small_blind_dealer = players[(dealer_index + 1) % player_count]  # type: ignore
        big_blind_dealer = players[(dealer_index + 2) % player_count]  # type: ignore

        blinds = sorted(state_after_hole_dealing.blinds_or_straddles)
        big_blind = blinds.pop()
        small_blind = blinds.pop()

        # announcing dealers and blind bets
        logs.append(f"{dealer} is the dealer.")
        logs.append(f"{small_blind_dealer} posts small blind - {small_blind} chips")
        logs.append(f"{big_blind_dealer} posts small blind - {big_blind} chips")

        logs.append("---")

        for index in range(player_count, len(actions)):
            action_log = actions[index]
            state = states[index]
            action_log = action_log.split(" ")

            if len(action_log) == 2:
                _, action = action_log

                # check or call : example log - p1 cc
                player, _ = action_log
                player_index = int(player[1]) - 1
                player = players[player_index]  # type: ignore
                if action == "cc":
                    if self.__bets_placed_before(state):
                        logs.append(f"{player} calls")
                    else:
                        logs.append(f"{player} checks")
                elif action == "f":
                    logs.append(f"{player} folds")

            elif len(action_log) == 3:
                _, action, _ = action_log

                if action == "db":  # deal board
                    _, _, cards = action_log
                    dealing_round_name = self.__get_dealing_round_name(state)
                    logs.append(f"{dealing_round_name} Dealt: {cards}")

                # complete bet or raise : example - < p1 cbr 8000 >
                elif action == "cbr":
                    player, _, amount = action_log
                    player_index = int(player[1]) - 1
                    player = players[player_index]  # type: ignore

                    if self.__bets_placed_before(state):
                        logs.append(f"{player} raises to {amount} chips")
                    else:
                        logs.append(f"{player} bets {amount} chips")

                elif action == "sm":  # show or muck
                    pass  # not part of log for now

        final_state = states[-1]
        allowed_actions = self.__get_allowed_actions(final_state)
        game_has_end = (
            not final_state.can_deal_board()
        ) and final_state.actor_index is None

        return (
            allowed_actions,
            logs,
            game_has_end,
            max([state.total_pot_amount for state in states]),
            # final_state.total_pot_amount,
            final_state.min_completion_betting_or_raising_to_amount or -1,
        )

    def __get_allowed_actions(self, state: State) -> List[ActionType]:
        allowed_actions = []
        # TODO: check should be done without the methods.

        for action_type in ActionType:
            allowed, _ = self.__can_perform_action(action_type, state)
            if allowed:
                allowed_actions.append(action_type)

        return allowed_actions

    def get_formatted_hand_history(self, hand: Hand) -> HandHistoryResponse:
        hand_history: HandHistory = self.__load_hand_history(hand)
        stack = hand_history.starting_stacks[0]
        players = hand_history.players
        states = [state for state, _ in hand_history.state_actions]
        player_count = len(players)  # type: ignore
        actions = hand_history.actions

        dealer_index = -1
        dealer_player = players[dealer_index]  # type: ignore
        small_blind_dealer = players[(dealer_index + 1) % player_count]  # type: ignore
        big_blind_dealer = players[(dealer_index + 2) % player_count]  # type: ignore

        final_state = states[-1]

        hands = {
            f"Player {index + 1}": f"{action.split()[3]}"
            for index, action in enumerate(actions[:player_count])
        }

        winnings = {
            f"Player {index + 1}": winning
            for index, winning in enumerate(final_state.payoffs)
        }

        actions = self.__get_formatted_hh_actions(hand)

        return HandHistoryResponse(
            id=hand.id,
            stack=stack,
            actions=actions,
            big_blind_player=big_blind_dealer,
            small_blind_player=small_blind_dealer,
            dealer=dealer_player,
            hands=hands,
            winnings=winnings,
        )

    def __get_formatted_hh_actions(self, hand: Hand) -> str:
        hand_history: HandHistory = self.__load_hand_history(hand)
        players = hand_history.players
        states = [state for state, _ in hand_history.state_actions]
        actions = hand_history.actions
        player_count = len(players)  # type: ignore

        logs = [[]]

        for index in range(player_count, len(actions)):
            action_log = actions[index]
            state = states[index]

            if action_log is None:
                continue

            action_log = action_log.split(" ")

            if len(action_log) == 2:
                _, action = action_log

                # check or call
                if action == "cc":
                    logs[-1].append("c" if self.__bets_placed_before(state) else "x")
                # fold
                elif action == "f":
                    logs[-1].append("f")

            elif len(action_log) == 3:
                _, action, _ = action_log

                # deal board : example - < d db 6hTs8s >
                if action == "db":
                    _, _, cards = action_log
                    logs.append([f"{cards}"])
                    logs.append([])

                # complete bet or raise : example - < p1 cbr 2000 >
                elif action == "cbr":
                    _, _, amount = action_log

                    if self.__bets_placed_before(state):
                        logs[-1].append(f"r{amount}")
                    else:
                        logs[-1].append(f"b{amount}")

        return " ".join([":".join(log) for log in logs])

    def __get_dealing_round_name(self, state: State) -> str:
        rounds = ["Flop", "Turn", "River"]
        board_cards = list(state.get_board_cards(0))

        return rounds[len(board_cards) - 3]

    def __bets_placed_before(self, state: State) -> bool:
        # at least one non zero bet
        return sum(state.bets) > 0

    def __can_perform_action(
        self, action: ActionType, state: State
    ) -> Tuple[bool, str]:
        if state.actor_index is None:
            return False, "Action not allowed. No active player."

        match action:
            case ActionType.FOLD:
                return True, "Action Allowed."

            case ActionType.CHECK:
                # No bets must be placed before for check to be allowed
                if not self.__bets_placed_before(state):
                    return True, "Action Allowed."
                return False, "Cannot check. A bet has been placed."

            case ActionType.CALL:
                # to call there has to be a bet placed before
                if self.__bets_placed_before(state):
                    return True, "Action Allowed."
                return False, "Cannot call. No bets placed before."

            case ActionType.BET:
                # to bet there should be no bets placed before
                if not self.__bets_placed_before(state):
                    return True, "Action Allowed."
                return (
                    False,
                    "Cannot bet. A bet has been placed before. You can only raise or call.",
                )

            case ActionType.RAISE:
                # to raise there should be a bet placed before
                if self.__bets_placed_before(state):
                    return True, "Action Allowed."
                return False, "Cannot raise. No bets placed before."

            case ActionType.ALLIN:
                # check if the player has enough chips to go all in
                if list(state.stacks)[state.actor_index] > 0:
                    return True, "Action Allowed."

                return (
                    False,
                    "Cannot go all in. Insufficient chips. You have run out of chips.",
                )

        return False, "Action not allowed. Unknown action type."

    def __dump_hand_history(self, state: State) -> str:
        game: NoLimitTexasHoldem = NoLimitTexasHoldem(
            automations=(
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.BOARD_DEALING,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_DEALING,
                Automation.ANTE_POSTING,
                Automation.BET_COLLECTION,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
                Automation.HAND_KILLING,
                Automation.CARD_BURNING,
            ),  # type: ignore
            ante_trimming_status=True,
            raw_antes={-1: 0},
            raw_blinds_or_straddles=(20, 40),
            min_bet=20,
            mode=Mode.CASH_GAME,
        )

        hand_history = HandHistory.from_game_state(game, state)
        hand_history.players = [f"Player {i+1}" for i in range(state.player_count)]
        buffer = io.BytesIO()
        hand_history.dump(buffer)
        game_str = buffer.getvalue().decode("utf-8")

        return game_str

    def __load_hand_history(self, hand: Hand) -> HandHistory:
        return HandHistory.load(io.BytesIO(bytes(hand.hand_history, encoding="utf-8")))
