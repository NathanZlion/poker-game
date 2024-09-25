
import { createSlice } from '@reduxjs/toolkit'


type playLogSliceState = {
    value: string[]
}

export const playLogSlice = createSlice({
    name: 'counter',
    initialState: {
        value: []
    },
    reducers: {
        addPlayLog: (state: playLogSliceState, action: { payload: string }) => {
            state.value = [...state.value, action.payload];
        },
        overwritePlayLog: (state, action) => {
            state.value = action.payload;
        }
    }
})

export const { addPlayLog, overwritePlayLog } = playLogSlice.actions
