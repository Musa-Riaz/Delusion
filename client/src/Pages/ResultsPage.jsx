import React, { useState } from "react";
import ResultCards from "@/Components/ResultCards";
import { Search, Plus } from "lucide-react";
import axios from "axios";
import { useSelector, useDispatch } from "react-redux";
import { setResultData } from "@/redux/slices/resultSlice";
import { Input } from "@/Components/ui/input";
import { Frown } from "lucide-react";
import { FaStar } from "react-icons/fa";
import { CiStar } from "react-icons/ci";
import { MoonLoader } from "react-spinners";
import { useEffect } from "react";
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
import { Upload } from "antd";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useToast } from "@/hooks/use-toast";

import { Button } from "@/components/ui/button";
import { Label } from "@radix-ui/react-label";
const ResultsPage = () => {
  const dispatch = useDispatch();
  const { toast } = useToast();
  const { Dragger } = Upload;
  const location = useLocation();
  let [page, setPage] = useState(1); // Pagination page number
  const [fileData, setFileData] = useState();
  const [articleUrl, setArticleUrl] = useState();
  const [files, setFiles] = useState([]);
  const navigate = useNavigate();
  const { results } = useSelector((state) => state.result);
  const { endLink } = useSelector((state) => state.result);
  const [query, setQuery] = useState(location?.state?.query); //intializing its value as the query passed from the home page
  const [loading, setLoading] = useState(false); // Loading state
  const [articleLoading, setArticleLoading] = useState(false);
  const [suggestions, setSuggestions] = useState([]); // Suggestions state
  const [selectedIndex, setSelectedIndex] = useState(-1);
  const [addMembersOnly, setAddMembersOnly] = useState(true);

  const handleSearch = async (newPage = 1, members_only = addMembersOnly) => {
    setLoading(true);
    setPage(newPage); // Set page number
    setSuggestions([]); // Clear suggestions after search
    try {
      const { data, status } = await axios.post(
        `http://localhost:8000/data?page=${newPage}&members_only=${members_only}`,
        {
          //will pass the page as a query parameter
          query,
        }
      );
      if (status == 200) {
        dispatch(setResultData(data.data));
        dispatch(setEndLink(data.totalPages)); //this state will be used to set the last page of the pagination
      }
    } catch (err) {
      console.log("page number", newPage);
      console.error("Error during search:", err);
    } finally {
      setLoading(false);
    }
  };

  const fetchSuggestions = async (value) => {
    if (!value.trim()) {
      setSuggestions([]); // Clear suggestions if the query is empty
      setSelectedIndex(-1);
      return;
    }
    try {
      const res = await axios.get(
        `http://localhost:8000/suggestions?query=${value}`
      );
      console.log(res.data);
      setSuggestions(res.data.suggestions);
      setSelectedIndex(res.data.suggestions.length > 0 ? 0 : -1);
    } catch (err) {
      console.log(err);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setPage(1); // Reset page to 1 for a new search
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    fetchSuggestions(value);
    setSelectedIndex(-1);
    setQuery(value);
  };

  const handlePageChange = (newPage) => {
    if (newPage > 0 && newPage <= endLink) {
      setPage(newPage);
      handleSearch(newPage);
    }
  };

  const handleFileChange = (e) => {
    const file = e.target.files[0]; // Get the selected file
    if (file) {
      const reader = new FileReader(); // Create a new FileReader
      reader.onload = (e) => {
        try {
          const json = JSON.parse(e.target.result); // Parse the file content
          console.log("Parsed JSON:", json);
          setFileData(json); // Set the parsed JSON data to state
        } catch (err) {
          console.error("Error parsing JSON file:", err);
        }
      };
      reader.readAsText(file); // Start reading the file as text
    } else {
      console.log("No file selected");
    }
  };

  const handleArticleSubmission = async (e) => {
    e.preventDefault();
    if (fileData) {
      try {
        setArticleLoading(true);
        const res = await axios.post(
          "http://localhost:8000/upload",
          { article: fileData },
          {
            headers: {
              "Content-Type": "application/json", // Ensure JSON content type
            },
          }
        );
        setArticleLoading(false);
        if (res.status == 200) {
          toast({
            title: "Success",
            description: "Article uploaded successfully",
            variant: "default",
          });
          setFileData(null);
          setFiles([]);
        }
      } catch (err) {
        setArticleLoading(false);
        console.log(err);
        toast({
          title: "Error",
          description: err.response.data.message,
          variant: "destructive",
        });
      }
    } else if (articleUrl) {
      try {
        setArticleLoading(true);
        const res = await axios.post("http://localhost:8000/upload/url", {
          query: articleUrl,
        });
        setArticleLoading(false);
        if (res.data.success) {
          toast({
            title: "Success",
            description: "Article uploaded successfully",
            variant: "default",
          });
          setArticleUrl("");
        } else {
          toast({
            title: "Error",
            description: res.data.message,
            variant: "destructive",
          });
        }
      } catch (err) {
        setArticleLoading(false);
        console.log(err);
        toast({
          title: "Error",
          description: "Wrong URL Format",
          variant: "destructive",
        });
      }
    }
  };

  const handleKeyDown = (e) => {
    if (suggestions.length > 0) {
      if (e.key === "ArrowDown") {
        setSelectedIndex((prevIndex) =>
          Math.min(prevIndex + 1, suggestions.length - 1)
        );
      } else if (e.key === "ArrowUp") {
        setSelectedIndex((prevIndex) => Math.max(prevIndex - 1, 0));
      } else if (e.key === "Tab") {
        e.preventDefault(); // Prevent default tab behavior
        if (selectedIndex >= 0) {
          const words = query.split(" ");
          words[words.length - 1] = suggestions[selectedIndex]; // Replace the last word
          setQuery(words.join(" ")); // Join the words back together
          setSuggestions([]); // Clear suggestions after selection
        }
      }
    }
    if (e.key === "Enter") {
      setPage(1); //reset the page to 1 whenever a new search is made

      handleSearch();
    }
  };

  useEffect(() => {
    handleSearch(1);
  }, [addMembersOnly]);
  

  return (
    <div className="bg-[#ffecd4] min-h-screen">
      <div className="p-2 flex gap-2 flex-col items-start  ">
        <Button onClick={() => navigate("/")}>Home</Button>
      </div>
      {/* Search Input Section */}
      <div className="flex justify-center items-center flex-col gap-22 p-10">
        <div className="w-[40vw] h-[7vh] flex rounded-lg border-4 border-black">
          <input
            type="text"
            placeholder="Type Anything"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown} // Trigger search on Enter key
            className="bg-[#ffecd4] w-full text-xl placeholder-black placeholder:text-xl p-3 focus:outline-none"
          />
          <span
            onClick={() => {
              setPage(1); //setting the page as 1 because the page number was being sent as an object
              handleSearch(); // Trigger search on click
            }}
            className="flex p-5 border-l-4 border-black items-center hover:shadow-2xl transition hover:cursor-pointer"
          >
            <Search />
          </span>
          <span className="flex p-5 border-l-4 bg-black  border-black items-center hover:shadow-2xl transition hover:cursor-pointer">
            <Dialog className="border ">
              <DialogTrigger>
                <Plus className="text-white" />
              </DialogTrigger>
              <DialogContent className="bg-[#ffecd4]">
                {articleLoading ? (
                  <div className="flex justify-center items-center w-full h-full">
                    <MoonLoader />
                  </div>
                ) : (
                  <>
                    <DialogTitle>Upload Your File Here</DialogTitle>
                    <form onSubmit={handleArticleSubmission}>
                      <div className="flex flex-col justify-center items-center gap-5 ">
                        <div className="flex flex-col items-center justify-center w-full p-6 border-2 border-dashed border-gray-600 rounded-lg bg-[#ffecd4] hover:border-gray-800">
                          <label
                            htmlFor="file-input"
                            className="flex flex-col items-center cursor-pointer"
                          >
                            <p className="text-gray-500">
                              Drag and drop your file here
                            </p>
                            <p className="text-sm text-gray-400">
                              or click to select files
                            </p>
                          </label>
                          <Input
                            id="file-input"
                            type="file"
                            accept=".json"
                            className="hidden "
                            onChange={(e) => {
                              handleFileChange(e);
                              setFiles([e.target.files[0]]);
                            }}
                          />
                          {files?.length > 0 && (
                            <ul className="mt-4 w-full text-sm text-gray-600">
                              {files?.map((file, index) => (
                                <li
                                  key={index}
                                  className="truncate border border-gray-300 bg-gray-100 rounded-md px-4 py-2 mb-2"
                                >
                                  {file.name}
                                </li>
                              ))}
                            </ul>
                          )}
                        </div>
                        OR
                        <Input
                          type="url"
                          placeholder="Enter your link here"
                          value={articleUrl}
                          onChange={(e) => setArticleUrl(e.target.value)}
                          className="bg-[#ffecd4] border border-black"
                        />
                      </div>
                      <div className="mt-3 flex justify-end">
                        <Button type="submit">Submit</Button>
                      </div>
                    </form>
                  </>
                )}
              </DialogContent>
            </Dialog>
          </span>
          <div className="flex items-center  ">
            <Label className="flex items-center gap-2 hover:cursor-pointer">
              <input
                type="checkbox"
                checked={addMembersOnly}
                onChange={() => {setAddMembersOnly(!addMembersOnly)
                }}
                className="hidden peer"
              />
              <div className="w-16 h-12 p-2 rounded-xs flex justify-center items-center :bg-[#ffecd4] peer-checked:bg-[#ffecd4]">
                {addMembersOnly ? <FaStar className=" text-yellow-400 w-24 h-24"/> 
              : <CiStar className="  w-24 h-24"/>  
              }
              </div>
            </Label>
          </div>
        </div>

        {/* Suggestions */}
        {suggestions.length > 0 && query.trim() && (
          <div
            style={{ top: "22%" }}
            className="absolute z-50 overflow-y-auto border p-2 w-[40vw] bg-white rounded-lg shadow-lg "
          >
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className={`p-2 hover:bg-gray-100 cursor-pointer ${
                  index === selectedIndex ? "bg-gray-300" : ""
                }`}
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </div>
            ))}
          </div>
        )}
        <h1 className="text-5xl font-myFont1 mt-10">
          The Top Search <span className="font-extrabold">Results</span> Are...
        </h1>
      </div>

      {/* Search Results Section */}
      <div className="flex flex-wrap justify-center p-5">
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
              authors={data.authors}
              data={data}
              members_only={data.members_only}
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
              {/* Previous Button */}
              <PaginationItem>
                <PaginationPrevious
                  className={`hover:cursor-pointer ${
                    page === 1 ? "opacity-50 pointer-events-none" : ""
                  }`}
                  onClick={() => handlePageChange(page - 1)}
                  disabled={page === 1}
                />
              </PaginationItem>

              {/* Page Numbers */}
              {(() => {
                const pagesToShow = 5; // Number of pages to show around the current page
                const pageNumbers = [];
                let startPage = Math.max(1, page - Math.floor(pagesToShow / 2));
                let endPage = Math.min(endLink, startPage + pagesToShow - 1);

                if (endPage - startPage < pagesToShow - 1) {
                  startPage = Math.max(1, endPage - pagesToShow + 1);
                }

                if (startPage > 1) {
                  pageNumbers.push(
                    <PaginationItem key={1}>
                      <PaginationLink
                        className="hover:cursor-pointer"
                        onClick={() => handlePageChange(1)}
                        isActive={page === 1}
                      >
                        1
                      </PaginationLink>
                    </PaginationItem>
                  );

                  if (startPage > 2) {
                    pageNumbers.push(
                      <PaginationItem key="start-ellipsis">
                        <PaginationEllipsis />
                      </PaginationItem>
                    );
                  }
                }

                for (let i = startPage; i <= endPage; i++) {
                  pageNumbers.push(
                    <PaginationItem key={i}>
                      <PaginationLink
                        className="hover:cursor-pointer"
                        onClick={() => handlePageChange(i)}
                        isActive={page === i}
                      >
                        {i}
                      </PaginationLink>
                    </PaginationItem>
                  );
                }

                if (endPage < endLink) {
                  if (endPage < endLink - 1) {
                    pageNumbers.push(
                      <PaginationItem key="end-ellipsis">
                        <PaginationEllipsis />
                      </PaginationItem>
                    );
                  }

                  pageNumbers.push(
                    <PaginationItem key={endLink}>
                      <PaginationLink
                        className="hover:cursor-pointer"
                        onClick={() => handlePageChange(endLink)}
                        isActive={page === endLink}
                      >
                        {endLink}
                      </PaginationLink>
                    </PaginationItem>
                  );
                }

                return pageNumbers;
              })()}

              {/* Next Button */}
              <PaginationItem>
                <PaginationNext
                  className={`hover:cursor-pointer ${
                    page === endLink ? "opacity-50 pointer-events-none" : ""
                  }`}
                  onClick={() => handlePageChange(page + 1)}
                  disabled={page === endLink}
                />
              </PaginationItem>
            </PaginationContent>
          </Pagination>
        </div>
      )}
    </div>
  );
};

export default ResultsPage;
