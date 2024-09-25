import { RootState } from '@/lib/store';
import { createAsyncThunk, createSlice, PayloadAction } from '@reduxjs/toolkit'


export type loadingTypes = "pending" | "idle" | "failed" | "success";

interface HandHistorySliceState {
    loading: loadingTypes
    value: string[]
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
        dispatch(handHistorySlice.actions.setLoading("pending"));
        console.log(getState());

    }
)
