import { configureStore } from "@reduxjs/toolkit";
import { resultSlice } from "./slices/resultSlice";

export default configureStore({
    reducer: {
        result: resultSlice.reducer
    }
})

