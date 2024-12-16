import React from "react";
import { Search } from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router";
const HomePage = () => {
  const navigate = useNavigate();

  const [query, setQuery] = useState("");
  const [results, setResults] = useState();
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    //will make the logic of fetching api data here
    //as the results will be fetched, direct the user to the results screen
    //send results as props to the results screen and display them there
    //also handle the logic, if query is empty, prompt the user to type something
    console.log("sending")
    if(query !== "") 
    navigate("/results");
  else
    alert("Please type something to search");

  }

  return (
    <div className="bg-[#ffecd4]">
      <div className="flex flex-col w-full md:flex-col gap-6 justify-center items-center flex-grow h-screen">
        {/* Graphics */}
        <div className="flex items-center  p-3">
          <div className="flex flex-col items-center">
            <div className="bg-[#ffc4cc] flex  items-center md:p-5 rounded-full ">
              <h1 className="md:text-6xl font-bold">Delusion</h1>
            </div>
            <h1 className=" md:text-6xl font-bold">Start Searching</h1>
          </div>
          <div>
            <img src="/12.png" alt="image" />
          </div>
        </div>
        {/* Search bar */}
        <div className="w-[50vw] h-[10vh] flex rounded-lg border-4  border-black ">
            <input type="text" placeholder="Type Anything" value={query} onChange={(e) => setQuery(e.target.value)} className="bg-[#ffecd4] w-full text-2xl placeholder-black placeholder:text-2xl p-3 focus:outline-none" />
            <span onClick={ handleSearch} className="flex p-5 border-l-4 border-black items-center hover:shadow-2xl transition hover:cursor-pointer"><Search/></span>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
