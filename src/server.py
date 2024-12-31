from file_handling import load_lexicon, load_scraped
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from search_util import get_results
from pydantic import BaseModel
from typing import Dict, Any
from fastapi import FastAPI
from fastapi import Query
import autocomplete as ac
import file_paths as fp
import threading as th
import indexer as idxr
from math import ceil
import scraper as sp
import uvicorn

print("Loading lexicon...")
lexicon = load_lexicon(fp.lexicon_file)
print("Creating autocomplete trie...")
lexicon_trie = ac.create_autocomplete_trie(100000, lexicon)
print("Loading scraped data...")
scraped = load_scraped(fp.scraped_file + '.csv')

app = FastAPI()

class ArticleData(BaseModel):
     article: Dict[str, Any] #idk what this is but apparently it is necessary if I want to send the data as json object

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
async def post_data(request : QueryData, page: int = 1, limit: int = 8, members_only: bool = False):
    query = request.query
    start_index = (page - 1) * limit
    end_index = start_index + limit
    results, total_results = get_results(query, lexicon, scraped, start_index, end_index, members_only)
    
    return JSONResponse({"success": True,
                          "data": results,
                          "totalResults": total_results,    #total number of results
                          "totalPages": ceil(total_results / limit),  #will need this for my pagination
                          "page": page,
                          "limit": limit,   #this is the limit, i.e the number of results per page
                          })

@app.post("/upload/url")
async def upload_url(request: QueryData):
    url = request.query
    article_data = sp.scrape_medium_article(url)
    
    try:
        article_data['thumbnail_url']
    except KeyError:
        return JSONResponse({"success": False,
                         "message": f"Error scraping URL: {article_data['details']}",
                          "url": url
                          })
    
    idxr.index_csv_dataset(article_data, lexicon, fp.ids_file, fp.forward_index_folder, fp.indexed_urls_file, fp.processed_docs_file, True, False)
    
    return JSONResponse({"success": True,
                         "message": "Article uploaded successfully",
                          "url": url
                          })

@app.post("/upload")
async def upload_article( request: ArticleData):
    article_data = request.article
    scraped_data = idxr.index_csv_dataset(article_data, lexicon, fp.ids_file, fp.forward_index_folder, fp.indexed_urls_file, fp.processed_docs_file, True, True)
    if scraped_data:
        return JSONResponse({"success": False,
                         "message": f"Error scraping URL: {scraped_data['details']}",
                          "data": article_data
                          })
    
    return JSONResponse({"success": True,
                         "message": "Article uploaded successfully",
                          "data": article_data
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
