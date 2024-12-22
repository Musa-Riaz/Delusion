import { createSlice } from "@reduxjs/toolkit";

export const resultSlice = createSlice({
    name: "result",
    initialState: {
        results: [],
        endLink:null
    },
    reducers: {
        setResultData: (state, action) => {
            state.results = action.payload;
        },
        setEndLink: (state, action) => {
            state.endLink = action.payload;
        }
    }
})

export const { setResultData, setEndLink } = resultSlice.actions;
export default resultSlice.reducer;
