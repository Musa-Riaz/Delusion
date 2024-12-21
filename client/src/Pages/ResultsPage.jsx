import React, { useState } from "react";
import ResultCards from "@/Components/ResultCards";
import { Search } from "lucide-react";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setResultData } from "@/redux/slices/resultSlice";
import { Frown } from "lucide-react";
import {PacmanLoader } from 'react-spinners'
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";

const ResultsPage = () => {
  const dispatch = useDispatch();
  let [page, setPage] = useState(1); // Pagination page number
  const [endLink, setEndLink] = useState();
  const {results} = useSelector((state) => state.result);
  const [query, setQuery] = useState(""); // Search query
  const [loading, setLoading] = useState(false); // Loading state

  const handleSearch = async (page = 1) => {
    setLoading(true);
    setPage(1);//reset the page to 1 whenever a new search is made
    try {
      const {data, status} = await axios.post(`http://localhost:8000/data?page=${page}`, { //will pass the page as a query parameter
        query, 
      });
      if(status == 200){
        dispatch(setResultData(data.data));
        setEndLink(data.totalPages) //this state will be used to set the last page of the pagination
      }
    } catch (err) {
      console.error("Error during search:", err);
    } finally {
      setLoading(false);
    }
  };

  const handlePageChange = (newPage) => {
    console.log(newPage)
    setPage(newPage);
    handleSearch(newPage);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="bg-[#ffecd4] min-h-screen">
      {/* Search Input Section */}
      <div className="flex justify-center items-center flex-col gap-6 p-10">
        <div className="w-[40vw] h-[6vh] flex rounded-lg border-4 border-black">
          <input
            type="text"
            placeholder="Type Anything"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
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
        <h1 className="text-5xl font-semibold">Results</h1>
      </div>

      {/* Search Results Section */}
      <div className="flex flex-wrap justify-between p-5">
        {loading ? (
          <div className="flex justify-center items-center w-full h-full">
            <PacmanLoader color="#000" size={60} />
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
        <div className="p-8 flex justify-center items-center border-black">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious className="hover:cursor-pointer" onClick={() => handlePageChange(page -1)}/>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => handlePageChange(page=1)}
              >
                1
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => handlePageChange(page=2)}
              >
                2
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink
                className="hover:cursor-pointer"
                onClick={() => handlePageChange(page=3)}
              >
                3
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationEllipsis />
            </PaginationItem>
            <PaginationItem>
              <PaginationLink onClick={() => handlePageChange(page=endLink)}>
                {endLink}
              </PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationNext className="hover:cursor-pointer"  onClick={() => handlePageChange(page+1)} />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
      )}
      
    </div>
  );
};

export default ResultsPage;
