import { apiService } from "@/lib/apiService";
import { RootState } from "@/lib/store";
import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { fetchHandHistory, loadingTypes } from "@/lib/feature/handHistory/handHistorySlice";


type HandSliceState = {
    handId: string | null,
    loading: loadingTypes,
    allowedActions: string[],
    stack: number,
    betSize: number,
    raiseSize: number,
    lastPotAmount: number,
    gameHasEnded: boolean,
    logs: string[]
}

interface actionPayload {
    actionType: actionSTypes,
    amount?: number
}

interface startHandResponse {
    id: string | null;
    allowed_actions: string[];
    message : string;
    logs: string[];
    game_has_ended: boolean;
    pot_amount: number;
}

interface performActionResponse {
    message: string;
    logs: string[];
    game_has_ended: boolean;
    allowed_actions: string[];
    pot_amount: number;
}

type actionSTypes = "FOLD" | "CHECK" | "CALL" | "BET" | "RAISE" | "ALLIN";

const initialState : HandSliceState = {
    handId: null,
    loading: "idle",
    allowedActions: [],
    stack: 1_000_000,
    betSize: 40,
    raiseSize: 40,
    lastPotAmount: 0,
    gameHasEnded: false,
    logs: []
};

export const handSlice = createSlice({
    name: 'hand',
    initialState: initialState,
    reducers: {
        increaseBetSize: (state, _) => {
            state.betSize += 40;
        },
        decreaseBetSize: (state, _) => {
            state.betSize -= 40;
        },
        increaseRaiseSize: (state, _) => {
            state.raiseSize += 40;
        },
        decreaseRaiseSize: (state, _) => {
            state.raiseSize -= 40;
        },
        setLoading: (state, action: PayloadAction<loadingTypes>) => {
            state.loading = action.payload;
        },
        setStack: (state, action: PayloadAction<number>) => {
            state.stack = action.payload;
        },
        setState: (state, action: PayloadAction<HandSliceState>) => {
            state.allowedActions=action.payload.allowedActions;
            state.gameHasEnded=action.payload.gameHasEnded;
            state.handId=action.payload.handId;
            state.logs=action.payload.logs;
        },
        reset: (state) => {
            state = initialState;
        }
    },
    extraReducers: (builder) => {
        builder.addCase(startHand.fulfilled, (state, action) => {
            state.loading = "success";
        }),
            builder.addCase(startHand.rejected, (state, action) => {
            state.loading = "failed";
        }),
        builder.addCase(performAction.fulfilled, (state, action) => {
            state.loading = "success";
        }),
            builder.addCase(performAction.rejected, (state, action) => {
            state.loading = "failed";
        })
    }
});


export const startHand = createAsyncThunk<void, number, { state: RootState }>(
    'hand/startHand',
    async (stack, { dispatch, getState }) => {
        
        // since we're starting a new game we should reset the handId
        dispatch(handSlice.actions.reset());

        dispatch(handSlice.actions.setLoading("pending"));
        const { data } = await apiService.post("/new_hand/", { stack });
        const {
            id,
            allowed_actions,
            logs,
            game_has_ended,
            pot_amount
        } = data as startHandResponse;

        const updatedState = {
            ...getState().hand,
            logs: logs,
            handId: id,
            allowedActions: allowed_actions,
            lastPotAmount: pot_amount,
            gameHasEnded: game_has_ended,
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
        })

        if (status !== 200) {
            dispatch(handSlice.actions.setLoading("failed"));
            return;
        }

        const { logs, allowed_actions, game_has_ended, pot_amount } = data as performActionResponse;

        const updatedState = {
            ...getState().hand,
            logs: logs,
            allowedActions: allowed_actions,
            gameHasEnded: game_has_ended,
            lastPotAmount: pot_amount
        }

        dispatch(handSlice.actions.setState(updatedState));

        // update the hand history to add the new hand
        if (game_has_ended) {
            dispatch(fetchHandHistory());
        }

        dispatch(handSlice.actions.setLoading("success"));
    }
);

