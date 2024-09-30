import { useToast } from '@/hooks/use-toast';
import { apiService } from '@/lib/apiService';
import { RootState } from '@/lib/store';
import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit'


export type loadingTypes = "pending" | "idle" | "failed" | "success";

interface HandHistory {
    id: number;
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

export const handHistorySlice = createSlice({
    name: 'counter',
    initialState: {
        loading: 'idle',
        value: []
    } as HandHistorySliceState,
    reducers: {
        setLoading: (state: HandHistorySliceState, action: PayloadAction<loadingTypes>) => {
            state.loading = action.payload;
        },
        setValue: (state: HandHistorySliceState, action: PayloadAction<HandHistory[]>) => {
            state.value = action.payload;
        }
    },
    extraReducers: (builder) => {
        builder.addCase(fetchHandHistory.fulfilled, (state: HandHistorySliceState, _) => {
            state.loading = "success";
        }),
            builder.addCase(fetchHandHistory.rejected, (state: HandHistorySliceState, _) => {
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
