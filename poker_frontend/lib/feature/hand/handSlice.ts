import { apiService } from "@/lib/apiService";
import { RootState } from "@/lib/store";
import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { fetchHandHistory, loadingTypes } from "@/lib/feature/handHistory/handHistorySlice";


type HandSliceState = {
    handId: string | null,
    loading: loadingTypes,
    allowedActions: string[],
    stack: number,
    raiseSize: number,
    betSize: number,
    pot_amount: number,
    gameHasEnded: boolean,
    logs: string[],
    minimum_bet_or_raise_amount: number
}

interface actionPayload {
    actionType: actionTypes,
    amount?: number
}

interface startHandResponse {
    id: string | null;
    allowed_actions: string[];
    message : string;
    logs: string[];
    game_has_ended: boolean;
    pot_amount: number;
    minimum_bet_or_raise_amount: number;
}

interface performActionResponse {
    message: string;
    logs: string[];
    game_has_ended: boolean;
    allowed_actions: string[];
    pot_amount: number;
    minimum_bet_or_raise_amount: number;
}

export type actionTypes = "FOLD" | "CHECK" | "CALL" | "BET" | "RAISE" | "ALL_IN";

const initialState : HandSliceState = {
    handId: null,
    loading: "idle",
    allowedActions: [],
    stack: 1_000_000,
    raiseSize: 40,
    betSize: 20,
    pot_amount: 0,
    gameHasEnded: false,
    logs: [],
    minimum_bet_or_raise_amount: 0
};

export const handSlice = createSlice({
    name: 'hand',
    initialState: initialState,
    reducers: {
        increaseBetSize: (state) => {
            state.betSize += 20;
        },
        decreaseBetSize: (state) => {
            state.betSize -= 20;
        },
        increaseRaiseSize: (state) => {
            state.raiseSize += 40;
        },
        decreaseRaiseSize: (state) => {
            state.raiseSize -= 40;
        },
        setLoading: (state, action: PayloadAction<loadingTypes>) => {
            state.loading = action.payload;
        },
        setStack: (state, action: PayloadAction<number>) => {
            state.stack = action.payload;
        },
        setState: (state, action: PayloadAction<HandSliceState>) => {
            state.allowedActions = action.payload.allowedActions;
            state.gameHasEnded = action.payload.gameHasEnded;
            state.handId = action.payload.handId;
            state.logs = action.payload.logs;
            state.minimum_bet_or_raise_amount = action.payload.minimum_bet_or_raise_amount;
            state.betSize = action.payload.minimum_bet_or_raise_amount;
            state.raiseSize = action.payload.minimum_bet_or_raise_amount;
            state.pot_amount = action.payload.pot_amount;
        },
    },
    extraReducers: (builder) => {
        builder.addCase(startHand.fulfilled, (state) => {
            state.loading = "success";
        }),
            builder.addCase(startHand.rejected, (state) => {
            state.loading = "failed";
        }),
        builder.addCase(performAction.fulfilled, (state) => {
            state.loading = "success";
        }),
            builder.addCase(performAction.rejected, (state) => {
            state.loading = "failed";
        })
    }
});


export const startHand = createAsyncThunk<void, number, { state: RootState }>(
    'hand/startHand',
    async (stack, { dispatch, getState }) => {
        dispatch(handSlice.actions.setLoading("pending"));
        const { status, data } = await apiService.post("/new_hand/", { stack });

        if (status !== 200) {
            dispatch(handSlice.actions.setLoading("failed"));
        }

        const {
            id,
            allowed_actions,
            logs,
            game_has_ended,
            pot_amount,
            minimum_bet_or_raise_amount
        } = data as startHandResponse;

        const updatedState = {
            ...getState().hand,
            logs: logs,
            handId: id,
            allowedActions: allowed_actions,
            lastPotAmount: pot_amount,
            gameHasEnded: game_has_ended,
            minimum_bet_or_raise_amount: minimum_bet_or_raise_amount
        };
        
        dispatch(handSlice.actions.setState(updatedState));
        dispatch(handSlice.actions.setLoading("success"));
    }
);



export const performAction = createAsyncThunk<void, actionPayload, { state: RootState }>(
    'hand/action',
    async ({ actionType, amount }, { dispatch, getState }) => {
        dispatch(handSlice.actions.setLoading("pending"));

        await new Promise((resolve) => setTimeout(resolve, 1000));

        const state = getState();
        const handId = state.hand.handId;

        const { data, status } = await apiService.post(`/hands/${handId}/actions`, {
            type: actionType,
            amount: amount
        });

        if (status !== 200) {
            dispatch(handSlice.actions.setLoading("failed"));
            return;
        }

        const { logs, allowed_actions, game_has_ended, pot_amount, minimum_bet_or_raise_amount } = data as performActionResponse;

        const updatedState = {
            ...getState().hand,
            logs: logs,
            allowedActions: allowed_actions,
            gameHasEnded: game_has_ended,
            pot_amount: pot_amount,
            minimum_bet_or_raise_amount: minimum_bet_or_raise_amount
        }

        dispatch(handSlice.actions.setState(updatedState));

        // update the hand history to add the new hand
        if (game_has_ended) {
            dispatch(fetchHandHistory());
        }

        dispatch(handSlice.actions.setLoading("success"));
    }
);


export const { increaseBetSize, decreaseBetSize, increaseRaiseSize, decreaseRaiseSize, setLoading, setStack } = handSlice.actions;