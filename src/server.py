from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from file_handling import load_lexicon
from search_util import get_results

NUM_RESULTS = 8
lexicon = load_lexicon(f'indexes/lexicon.csv')

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)

class QueryData(BaseModel):
    query: str

@app.post("/data")
async def post_data(request : QueryData):
    query = request.query
    results = get_results(query, NUM_RESULTS, lexicon)
    return JSONResponse({"message": "success", "success": True, "data": results})

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
