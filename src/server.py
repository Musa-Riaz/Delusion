from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
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
    doc_dict['timeStamps'] = ['now', 'then']
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

NUM_RESULTS = 8
@app.post("/data")
async def post_data(request : QueryData):
    query = request.query
    docs = search_util.get_word_docs(query)
    results = []
    if docs:
        for i in range(min(NUM_RESULTS, len(docs))):
            this_doc = search_util.get_doc_info(docs[i][0])
            results.append(convert_to_json(this_doc))

    return JSONResponse({"message": "success", "success": True, "data": results})

if __name__ == "__main__":
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
