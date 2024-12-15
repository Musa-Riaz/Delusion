import React from "react";
import { Search } from "lucide-react";
const HomePage = () => {
  return (
    <div className="bg-[#ffecd4]">
      <div className="flex flex-col gap-6 justify-center items-center flex-grow h-screen">
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
            <input type="text" placeholder="Type Anything" className="bg-[#ffecd4] w-full text-2xl placeholder-black placeholder:text-2xl p-3 focus:outline-none" />
            <span className="flex p-5 border-l-4 border-black items-center hover:cursor-pointer"><Search/></span>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
