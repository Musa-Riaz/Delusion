from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from file_handling import load_lexicon
from search_util import get_results
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import Query
import autocomplete as ac
from math import ceil
import uvicorn

print("Loading lexicon...")
lexicon = load_lexicon(f'indexes/lexicon.csv')
print("Creating autocomplete trie...")
lexicon_trie = ac.create_autocomplete_trie(100000, lexicon)

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
async def post_data(request : QueryData, page: int = 1, limit: int = 8):
    query = request.query
    start_index = (page - 1) * limit
    end_index = start_index + limit
    results, total_results = get_results(query, lexicon, start_index, end_index)
    
    return JSONResponse({"success": True,
                          "data": results,
                          "totalResults": total_results,    #total number of results
                          "totalPages": ceil(total_results / limit),  #will need this for my pagination
                          "page": page,
                          "limit": limit,   #this is the limit, i.e the number of results per page
                          })

@app.get("/suggestions")
async def get_suggestions(query: str = Query(..., min_length=1, description="Search query"), limit: int = 10):
    try:
        if query[-1] == ' ':
            query = ''
        else:
            query = query.split(' ')[-1]
        suggestions = ac.get_suggestions(lexicon_trie, lexicon, query, limit)
        return JSONResponse(content={"suggestions":suggestions})
    except Exception as e:
         return JSONResponse(content={"error": str(e)}, status_code=500)
   
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
