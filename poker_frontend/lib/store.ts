import { configureStore } from '@reduxjs/toolkit'
import { handHistorySlice } from '@/lib/feature/handHistory/handHistorySlice';
import { handSlice } from '@/lib/feature/hand/handSlice';

export const makeStore = () => {
  return configureStore({
    reducer: {
      hand: handSlice.reducer,
      history: handHistorySlice.reducer
    }
  })
}

// Infer the type of makeStore
export type AppStore = ReturnType<typeof makeStore>;

// Infer the `RootState` and `AppDispatch` types from the store itself
export type RootState = ReturnType<AppStore['getState']>;
export type AppDispatch = AppStore['dispatch'];


// Can still subscribe to the store
// makeStore.subscribe(() => console.log(makeStore.getState()))

// Still pass action objects to `dispatch`, but they're created for us
// makeStore.dispatch(incremented())
// // {value: 1}
// makeStore.dispatch(incremented())
// // {value: 2}
// makeStore.dispatch(decremented())
// // {value: 1}