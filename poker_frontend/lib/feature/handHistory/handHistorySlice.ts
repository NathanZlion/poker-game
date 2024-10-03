import { apiService } from '@/lib/apiService';
import { RootState } from '@/lib/store';
import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit'


export type loadingTypes = "pending" | "idle" | "failed" | "success";

interface HandHistory {
    id: string;
    small_blind_player: string;
    stack: number;
    big_blind_player: string;
    hands: Map<string, string>;
    winnings: Map<string, number>;
    dealer: string;
    actions: string;
}

interface HandHistorySliceState {
    loading: loadingTypes
    value: HandHistory[]
}


const initialState: HandHistorySliceState = {
    loading: 'idle',
    value: []
};

export const handHistorySlice = createSlice({
    name: 'counter',
    initialState: initialState,
    reducers: {
        setLoading: (state: HandHistorySliceState, action: PayloadAction<loadingTypes>) => {
            state.loading = action.payload;
        },
        setValue: (state: HandHistorySliceState, action: PayloadAction<HandHistory[]>) => {
            state.value = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder.addCase(fetchHandHistory.fulfilled, (state: HandHistorySliceState) => {
            state.loading = "success";
        }),
            builder.addCase(fetchHandHistory.rejected, (state: HandHistorySliceState) => {
                state.loading = "failed";
            })
    }
});


export const fetchHandHistory = createAsyncThunk<void, void, { state: RootState }>(
    'handHistory/fetchHandHistory',
    async (_, { dispatch, getState }) => {

        // another reload is in progress
        if (getState().history.loading === "pending") {
            return;
        }
        
        dispatch(handHistorySlice.actions.setLoading("pending"));
        
        // Fetch history from server
        const { data, status } = await apiService.get("/hands");

        if (status !== 200) {
            dispatch(handHistorySlice.actions.setLoading("failed"));
            return;
        }

        // Update store
        dispatch(handHistorySlice.actions.setValue(data));

        dispatch(handHistorySlice.actions.setLoading("success"));
    }
)
