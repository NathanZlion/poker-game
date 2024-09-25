import { apiService } from "@/lib/apiService";
import { RootState } from "@/lib/store";
import { createAsyncThunk, createSlice, PayloadAction } from "@reduxjs/toolkit";
import { loadingTypes } from "@/lib/feature/handHistory/handHistorySlice";


type HandSliceState = {
    handId: string | null,
    loading: loadingTypes,
    betSize: number,
    raiseSize: number,
    canFold: boolean,
    canCheck: boolean,
    canCall: boolean,
    canRaise: boolean,
    canBet: boolean,
    canAllIn: boolean,
}

interface actionPayload {
    actionType: actionSTypes,
    amount?: number
}

type actionSTypes = "Fold" | "Check" | "Call" | "Bet" | "Raise" | "AllIn";

export const handSlice = createSlice({
    name: 'hand',
    initialState: {
        handId: null,
        raiseSize: 40,
        loading: "idle",
        betSize: 40,
        bigBlindSize: 10,
        canFold: false,
        canCheck: false,
        canCall: false,
        canRaise: false,
        canBet: false,
        canAllIn: false,
    } as HandSliceState,
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
            console.log(action.payload);    
            state.loading = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder.addCase(action.fulfilled, (state, action) => {
            state.loading = "success";
        }),
            builder.addCase(action.rejected, (state, action) => {
            state.loading = "failed";
        })
    }
});


export const action = createAsyncThunk<void, actionPayload, { state: RootState }>(
    'hand/action',
    async ({ actionType }, { dispatch, getState }) => {
        console.log(actionType);
        dispatch(handSlice.actions.setLoading("pending"));

        await new Promise((resolve) => setTimeout(resolve, 1000));

        dispatch(handSlice.actions.setLoading("success"));


        // const state = getState(); 
        // const handId = state.hand.handId;

        // const result = await apiService.post("", {});
    }
);


// export const 
