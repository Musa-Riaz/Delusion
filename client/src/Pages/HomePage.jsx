import React from "react";
import axios from "axios";
import { Search } from "lucide-react";
import { useState } from "react";
import { setEndLink } from "../redux/slices/resultSlice";
import { useNavigate } from "react-router";
import { useSelector, useDispatch } from "react-redux";
import { MoonLoader } from "react-spinners";
import { setResultData } from "../redux/slices/resultSlice";
const HomePage = () => {
  const [page, setPage] = useState(1); // Pagination page number
  const [suggestions, setSuggestions] = useState([]); // Suggestions state
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [selectedIndex, setSelectedIndex] = useState(-1);

  const handleSearch = async (page = 1) => {
    setLoading(true);

    try {
      setLoading(true);
      setSuggestions([]); // Clear suggestions after search
      const { data, status } = await axios.post(
        `http://localhost:8000/data?page=${page}`,
        {
          //will pass the page as a query parameter
          query,
        }
      );
      setLoading(false);
      if (status == 200) {
        dispatch(setResultData(data.data));
        dispatch(setEndLink(data.totalPages));
      }
    } catch (err) {
      setLoading(false);
      console.error("Error during search:", err);
    } finally {
      setLoading(false);
      navigate("/results", { state: { query } });
    }
  };

  const fetchSuggestions = async (value) => {
    console.log(value);
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
      setSelectedIndex(res.data.suggestions.length > 0 ? 0 : -1)
    } catch (err) {
      console.log(err);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setPage(1); // Reset page to 1 for a new search
    // handleSearch(1);
  };

  const handleInputChange = (e) => {
    const value = e.target.value;
    fetchSuggestions(value);
    setSelectedIndex(-1);
    setQuery(value);
  };

  const handleKeyDown = (e) => {
    if (suggestions.length > 0) {
      if (e.key === "ArrowDown" || e.key === "W") {
        setSelectedIndex((prevIndex) =>
          Math.min(prevIndex + 1, suggestions.length - 1)
        );
      } else if (e.key === "ArrowUp" || e.key === "S") {
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

  return (
    <div className="bg-[#ffecd4] ">
      <div className="flex flex-col w-full md:flex-col gap-6 justify-center items-center flex-grow h-screen">
        {/* Graphics */}
        <div className="flex items-center gap-12">
          <div className="flex flex-col items-center">
            <div className="bg-[#ffc4cc] flex  items-center md:p-5 rounded-full ">
              <h1 className="md:text-6xl font-bold">Delusion</h1>
            </div>
            <h1 className=" md:text-6xl font-bold">Start Searching</h1>
          </div>
          <div>
            <img src="/home.png" alt="image" />
          </div>
        </div>
        {/* Search bar */}
        <div className="w-[50vw] h-[10vh] flex rounded-lg border-4  border-black ">
          <input
            type="text"
            placeholder="Type Anything"
            value={query}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            className="bg-[#ffecd4] w-full text-2xl placeholder-black placeholder:text-2xl p-3 focus:outline-none"
          />
          <span
            onClick={() => {
              setPage(1); //setting the page as 1 because the page number was being sent as an object 
              handleSearch();
            }}
            className="flex p-5 border-l-4 border-black items-center hover:shadow-2xl transition hover:cursor-pointer"
          >
            <Search />
          </span>
        </div>
        {/* Suggestions */}
        {suggestions.length > 0 && query.trim() && (
          <div
            style={{ bottom: "3%" }}
            className="w-[51vw] mt-2 p-2 relative z-50  bg-white rounded-lg shadow-lg "
          >
            {suggestions.map((suggestion, index) => (
              <div
                key={index}
                className={`p-2 hover:bg-gray-100 cursor-pointer ${
                  index === selectedIndex ? "bg-gray-300 rounded-lg" : ""
                }`}
                onClick={() => handleSuggestionClick(suggestion)}
              >
                {suggestion}
              </div>
            ))}
          </div>
        )}

        {loading && (
          <div className="flex justify-center items-center ">
            <MoonLoader color="#000" size={50} />
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
