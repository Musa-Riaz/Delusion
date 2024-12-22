from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from math import ceil
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
async def post_data(request : QueryData, page: int = 1, limit: int = 8):
    query = request.query
    docs = search_util.get_word_docs(query)
    total_results = len(docs)
    start_index = (page - 1)* limit #eg if page is 1 then 0*8 = 0
    end_index = start_index + limit # similarly 0 + 8 = 8
    paginated_docs = docs[start_index:end_index] #so give us pages in the range of 0 to 8
    results = [convert_to_json(search_util.get_doc_info(doc[0])) for doc in paginated_docs]
    
    return JSONResponse({"success": True,
                          "data": results,
                          "totalResults": total_results, #total number of results
                          "totalPages": ceil(total_results/limit), #will need this for my pagination
                          "page": page,
                          "limit": limit,#this is the limit, i.e the number of results per page
                          })

@app.get("/suggestions")
async def get_suggestions(query: str = Query(..., min_length=1, description="Search query"), limit: int = 10):
    try:
        lexicon = fh.load_lexicon('indexes/lexicon.csv')
        suggestions = [word for word in lexicon.keys() if word.lower().startswith(query.lower())]

        return JSONResponse(content={"suggestions":suggestions[:limit]})
    except Exception as e:
         return JSONResponse(content={"error": str(e)}, status_code=500)
   
if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
