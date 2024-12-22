import React, { useState } from "react";
import ResultCards from "@/Components/ResultCards";
import { Search } from "lucide-react";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setResultData } from "@/redux/slices/resultSlice";
import { Frown } from "lucide-react";
import {MoonLoader } from 'react-spinners'
import { useLocation } from "react-router";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
import { useNavigate } from "react-router";
import { setEndLink } from "@/redux/slices/resultSlice";
import {Button} from '@/components/ui/button'
const ResultsPage = () => {
  const dispatch = useDispatch();
  const location = useLocation();
  let [page, setPage] = useState(1); // Pagination page number
  const navigate = useNavigate();
  const {results} = useSelector((state) => state.result);
  const {endLink} = useSelector((state) => state.result);
  const [query, setQuery] = useState(location?.state?.query); //intializing its value as the query passed from the home page
  const [loading, setLoading] = useState(false); // Loading state
  const [suggestions, setSuggestions] = useState([]); // Suggestions state

  const handleSearch = async (newPage = page) => {
    setLoading(true);
    setSuggestions([]); // Clear suggestions after search
    try {
      const {data, status} = await axios.post(`http://localhost:8000/data?page=${newPage}`, { //will pass the page as a query parameter
        query, 
      });
      if(status == 200){
        
        dispatch(setResultData(data.data));
        dispatch(setEndLink(data.totalPages)) //this state will be used to set the last page of the pagination
      } 
    } catch (err) {
      console.log('page number', newPage)
      console.error("Error during search:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSuggestions = async (value) => {
    if (!value.trim()) {
      setSuggestions([]); // Clear suggestions if the query is empty
      return;
    }
    try{
      const res = await axios.get(`http://localhost:8000/suggestions?query=${query}`);
      console.log(res.data);
      setSuggestions(res.data.suggestions);
    }
    catch(err){
      console.log(err);
    }
  
  }

  const handleSuggestionClick = (suggestion) => {
   
    setQuery(suggestion);
    setPage(1); // Reset page to 1 for a new search
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    setQuery(value);
    fetchSuggestions(value)
  }

  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= endLink){
    setPage(newPage);
    handleSearch(newPage);
    }
    
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      setPage(1);//reset the page to 1 whenever a new search is made
      handleSearch();
    }
  };

  return (
    <div className="bg-[#ffecd4] min-h-screen">
      <div className=" p-2">
      <Button onClick={()=>navigate('/')}>Home</Button>
      </div>
      {/* Search Input Section */}
      <div className="flex justify-center items-center flex-col gap-6 p-10">
        <div className="w-[40vw] h-[6vh] flex rounded-lg border-4 border-black">
          <input
            type="text"
            placeholder="Type Anything"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown} // Trigger search on Enter key
            className="bg-[#ffecd4] w-full text-xl placeholder-black placeholder:text-xl p-3 focus:outline-none"
          />
          <span
            onClick={handleSearch} // Trigger search on click
            className="flex p-5 border-l-4 border-black items-center hover:shadow-2xl transition hover:cursor-pointer"
          >
            <Search />
          </span>

        </div>
          {/* Suggestions */}
          {suggestions.length > 0 && query.trim() && (
            <div style={{ top: '19%' }} className="absolute z-50 overflow-y-auto border p-2 w-[40vw] bg-white rounded-lg shadow-lg ">
              {suggestions.map((suggestion, index) => (
                <div key={index} className="p-2 hover:bg-gray-100 cursor-pointer" onClick={() => handleSuggestionClick(suggestion)}>
                  {suggestion}
                </div>
              ))}
            </div>
          )}
        <h1 className="text-5xl font-semibold">Results</h1>
      </div>

      {/* Search Results Section */}
      <div className="flex flex-wrap justify-between p-5">
        {loading ? (
          <div className="flex justify-center items-center w-full h-full">
            <MoonLoader color="#000" size={60} />
          </div> // Show loading text while fetching results
        ) : results.length > 0 ? (
          results.map((data, index) => (
            <ResultCards
              key={index}
              title={data.title}
              description={data.description}
              url={data.url}
              imageUrl={data?.imageUrl}
              tags={data.tags}
              timeStamps={data.timeStamps}
              data={data}
            />
          ))
        ) : (
          <div className="flex justify-center items-center flex-col gap-5 w-full h-full">  
            <p className="text-2xl font-bold">No results found</p>
            <Frown size={40} />
          </div>
        )}
      </div>

      {/* Pagination */}
      {results.length > 0 && (
        <div className="p-8 flex justify-center items-center border-black ">
        <Pagination>
          <PaginationContent>
            {page !== 1 ? (
                          <PaginationItem >
                          <PaginationPrevious className="hover:cursor-pointer" onClick={() => handlePageChange(page -1)}/>
                        </PaginationItem>
            ) : null}
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => {handlePageChange(page=1)}}
                isActive={page === 1}
              >
                1
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => handlePageChange(page=2)}
                isActive={page === 2}
              >
                2
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => handlePageChange(page=3)}
                isActive={page === 3}
              >
                3
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationEllipsis />
            </PaginationItem>
            <PaginationItem>
              <PaginationLink  className="hover:cursor-pointer" onClick={() => handlePageChange(page=endLink)} isActive={page === endLink}>
                {endLink}
              </PaginationLink>
            </PaginationItem>
            {page !== endLink ? (
              <PaginationItem>
              <PaginationNext className="hover:cursor-pointer"  onClick={() => handlePageChange(page+1)} />
            </PaginationItem>
            ) : null}
          </PaginationContent>
        </Pagination>
      </div>
      )}
      
    </div>
  );
};

export default ResultsPage;
