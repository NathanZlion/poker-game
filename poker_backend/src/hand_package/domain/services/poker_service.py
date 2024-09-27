import io
from typing import List, Tuple
from src.hand_package.domain.entities.hand import Hand
from src.hand_package.domain.value_objects.action import Action, ActionObject, ActionType
from src.hand_package.domain.value_objects.hand import CreateHand
from pokerkit import Automation, NoLimitTexasHoldem, State, Mode, HandHistory

from src.hand_package.presentation.schema.action import ActionResponse


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
            ), # type: ignore
            ante_trimming_status=True,
            raw_antes={-1: 0},
            raw_blinds_or_straddles=(1000, 2000),
            min_bet=2000,
            raw_starting_stacks=[create_hand.stack_size for _ in range(create_hand.player_count)],
            mode=Mode.CASH_GAME,
            player_count=create_hand.player_count
        )

        # call the repository to create a hand
        return Hand(
            game_has_ended=False,
            hand_history=self.__dump_hand_history(state),
        )

    def perform_action_on_hand(self, action: Action, hand: Hand) -> Tuple[ActionResponse, Hand]:
        allowed_actions, logs, game_has_ended, total_pot_size = self.analyse_hand(hand)
        hand_history = self.__load_hand_history(hand)
        final_state = [state for state, _ in hand_history.state_actions ][-1]

        if game_has_ended:
            return ActionResponse(
                success=False,
                message="Game has ended.",
                allowed_moves=[],
                game_has_ended=game_has_ended,
                logs=logs,
                pot_amount=total_pot_size,
            ), hand

        # check if the action can be performed
        if not self.__can_perform_action(action, hand):

            print(logs)
            print(final_state.payoffs)

            return ActionResponse(
                id=hand.id,
                success=False,
                message="Invalid Action.",
                allowed_moves=allowed_actions,
                game_has_ended=game_has_ended,
                logs=logs,
                pot_amount=total_pot_size,
            ), hand

        match action.type:
            case ActionType.FOLD:
                final_state.fold()

            case ActionType.CHECK |  ActionType.CALL:
                final_state.check_or_call()

            case ActionType.BET | ActionType.RAISE | ActionType.ALLIN:
                final_state.complete_bet_or_raise_to(action.amount)

        updated_hand_history = self.__dump_hand_history(final_state)
        hand.hand_history = updated_hand_history
        allowed_actions, logs, game_has_ended, total_pot_size = self.analyse_hand(hand)
        hand.game_has_ended = game_has_ended

        hand_history = self.__load_hand_history(hand)
        final_state = [state for state, _ in hand_history.state_actions ][-1]
        if final_state.can_deal_board():
            final_state.deal_board()

        updated_hand_history = self.__dump_hand_history(final_state)
        hand.hand_history = updated_hand_history
        allowed_actions, logs, game_has_ended, total_pot_size = self.analyse_hand(hand)
        hand.game_has_ended = game_has_ended

        print("________________ IN PERFORM ACTION ON HAND __________________")
        print("Action performed: ", action.type)
        print(self.formatState(final_state))


        return ActionResponse(
            id=hand.id,
            success=True,
            message="Action performed successfully.",
            allowed_moves=allowed_actions,
            game_has_ended=game_has_ended,
            logs=logs,
            pot_amount=total_pot_size,
        ), hand

    def analyse_hand(self, hand: Hand) -> Tuple[List[ActionType], List[str], bool, int]:
        """Analyse Hand

        returns : allowed_actions, logs, game_has_ended, total_pot_size
        """
        logs = []
        hand_history = self.__load_hand_history(hand)
        players = hand_history.players
        states = [state for state, _ in hand_history.state_actions]
        actions = hand_history.actions
        # [action for _, action in hand_history.state_actions]
        player_count = len(players) # type: ignore

        # log of the hole dealing
        state_after_hole_dealing = states[player_count]

        for index, cards in enumerate(state_after_hole_dealing.hole_cards):
            logs.append(f"Player {index + 1} is dealt {cards}")

        # for state, action in hand_history.state_actions:
        #     print(self.formatState(state))
        #     print(action)

        # ----
        logs.append("---")

        dealer_index = -1
        dealer = players[dealer_index]  # type: ignore
        small_blind_dealer = players[(dealer_index + 1) % player_count]  # type: ignore
        big_blind_dealer = players[(dealer_index + 2) % player_count]  # type: ignore

        blinds = sorted(state_after_hole_dealing.blinds_or_straddles)
        big_blind = blinds.pop()
        small_blind = blinds.pop()

        # small_blind, big_blind, _ = state_after_hole_dealing.blinds_or_straddles

        # announcing dealers and blind bets
        logs.append(f"{dealer} is the dealer.")
        logs.append(f"{small_blind_dealer} posts small blind - {small_blind} chips")
        logs.append(f"{big_blind_dealer} posts small blind - {big_blind} chips")

        logs.append("---")

        print(actions)
        for index in range(player_count, len(actions)):
            action_log = actions[index]

            if action_log is None:
                continue

            action_log = action_log.split(" ")

            if len(action_log) == 2:
                _, action = action_log
                state = states[index]

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

                # complete bet or raise : example -
                elif action == "cbr":  
                    player, _, amount = action_log
                    player_index = int(player[1]) - 1
                    player = players[player_index]  # type: ignore

                    if self.__bets_placed_before(state):
                        logs.append(f"{player} raises to {amount} chips")
                    else:
                        logs.append(f"{player} bets {amount} chips")

                elif action == "sm":  # show or muck
                    pass    # not part of log for now

        final_state = states[-1]
        allowed_actions = self.__get_allowed_actions(final_state)
        game_has_end = not (final_state.can_deal_board() or  final_state.actor_index is not None)
        print("__ GAME HAS ENDED __", game_has_end)
        return allowed_actions, logs, game_has_end, final_state.total_pot_amount

    def __get_allowed_actions(self, state: State) -> List[ActionType]:
        allowed_actions = []

        for action_type in ActionType:
            match action_type:
                case ActionType.FOLD:
                    if state.can_fold():
                        allowed_actions.append(action_type)

                case ActionType.CHECK |  ActionType.CALL:
                    if state.can_check_or_call():
                        allowed_actions.append(action_type)

                case ActionType.BET | ActionType.RAISE | ActionType.ALLIN:
                    if state.can_complete_bet_or_raise_to():
                        allowed_actions.append(action_type)

        return allowed_actions

    def __get_dealing_round_name(self, state: State) -> str:
        rounds = ["Flop", "Turn", "River"]
        board_cards = list(state.get_board_cards(0))

        return rounds[len(board_cards) - 3]

    def __bets_placed_before(self, state: State) -> bool:
        # at least one non zero bet
        return any(state.bets)

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

    # def get_allowed_actions(self, hand: Hand) -> List[ActionType]:
    #     allowed_actions = []

    #     for action_type in ActionType:
    #         action: Action = Action(
    #             hand_id=hand.id, type=action_type, amount=0, description=""
    #         )
    #         if self.__can_perform_action(action, hand):
    #             allowed_actions.append(action_type)

    #     return allowed_actions

    def __dump_hand_history(self, state: State) -> str:
        game : NoLimitTexasHoldem = NoLimitTexasHoldem(
            automations=(
                Automation.BOARD_DEALING,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_DEALING,
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
        print("_DUMP HISTORY", hand_history.actions)
        hand_history.players = [f"Player {i+1}" for i in range(state.player_count)]
        buffer = io.BytesIO()
        hand_history.dump(buffer)
        game_str = buffer.getvalue().decode('utf-8')

        return game_str

    def __load_hand_history(self, hand: Hand) -> HandHistory:
        return HandHistory.load(io.BytesIO(bytes(hand.hand_history, encoding="utf-8")))

    def formatState(self, state: State) -> str:
        res = []
        res.append(f"Actor_indices: {state.actor_indices}, active player: {state.actor_index}\n")
        res.append(f"Stacks: {state.stacks}\n")
        res.append(f"Bets: {state.bets}\n")
        res.append(f"Total Pot Amount: {state.total_pot_amount}\n")
        res.append(f"Hole Cards {state.hole_cards}\n")
        res.append(f"Pot Amounts: {tuple(state.pot_amounts)}\n")
        res.append(f"Minimum Completion/Raise Betting: {state.min_completion_betting_or_raising_to_amount}\n")
        res.append(f"Board : {tuple(state.get_board_cards(0))}\n")
        res.append(f"Can deal : {state.can_deal_board()}\n")
        res.append(f"Status : {state.status}\n")

        return "".join(res)

    # def __get_history_from_hand_history(self, hand_history: HandHistory) -> str:
    #     buffer = io.BytesIO()
    #     hand_history.dump(buffer)
    #     game_str = buffer.getvalue().decode('utf-8')
    #     return game_str
