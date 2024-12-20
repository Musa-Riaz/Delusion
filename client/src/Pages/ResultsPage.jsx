import React, { useState } from "react";
import ResultCards from "@/Components/ResultCards";
import { Search } from "lucide-react";
import axios from "axios";
import { useEffect } from "react";
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
  const [query, setQuery] = useState(""); // Search query
  const [result, setResult] = useState([]); // Search results
  const [loading, setLoading] = useState(false); // Loading state

  const handleSearch = async () => {
    setLoading(true);
    try {
      const {data, status} = await axios.post("http://localhost:8000/data", {
        "query": query
      });
      console.log('data', data.data)
      if(status == 200)
      setResult(data.data)
    } catch (err) {
      console.error("Error during search:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter") {
      handleSearch();
    }
  };

  return (
    <div className="bg-[#ffecd4]">
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
          <p>Loading...</p> // Show loading text while fetching results
        ) : result.length > 0 ? (
          result.map((data, index) => (
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
          <p>No results found.</p> // Fallback message for no results
        )}
      </div>

      {/* Pagination */}
      <div className="p-8 flex justify-center items-center border-black">
        <Pagination>
          <PaginationContent>
            <PaginationItem>
              <PaginationPrevious href="#" />
            </PaginationItem>
            <PaginationItem>
              <PaginationLink href="#">1</PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink href="#">2</PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationLink href="#">3</PaginationLink>
            </PaginationItem>
            <PaginationItem>
              <PaginationEllipsis />
            </PaginationItem>
            <PaginationItem>
              <PaginationNext href="#" />
            </PaginationItem>
          </PaginationContent>
        </Pagination>
      </div>
    </div>
  );
};

export default ResultsPage;
