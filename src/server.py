from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from math import ceil
import uvicorn
from pydantic import BaseModel
import search_util

def convert_to_json(doc):
    doc_dict = {}
    doc_dict['title'] = doc[1]
    doc_dict['url'] = doc[2]
    doc_dict['description'] = 'THIS IS DESCRIPTION HEHE'
    doc_dict['imageUrl'] = 'https://creatorset.com/cdn/shop/files/Screenshot_2024-04-24_173231_1114x.png?v=1713973029'
    doc_dict['tags'] = doc[4]
    doc_dict['timeStamps'] = ['now']
    return doc_dict

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

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
