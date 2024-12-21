import { createSlice } from "@reduxjs/toolkit";

export const resultSlice = createSlice({
    name: "result",
    initialState: {
        results: []
    },
    reducers: {
        setResultData: (state, action) => {
            state.results = action.payload;
        }
    }
})

export const { setResultData } = resultSlice.actions;
export default resultSlice.reducer;
