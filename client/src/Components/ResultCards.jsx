import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";


const ResultCards = ({
  title,
  description,
  url,
  imageUrl,
  tags,
  timeStamps,
  authors,
  data
}) => {

  return (
    <div className="flex p-4">
      <Card className="w-[380px] flex flex-col overflow-hidden border rounded-lg shadow-lg transition-transform transform hover:scale-105 duration-200 ease-in-out">
        <CardHeader className="p-4  h-24">
          <CardTitle className="text-lg line-clamp-2 overflow-hidden text-ellipsis font-bold ">{title}</CardTitle>
        </CardHeader>
        <CardContent className="p-4">
          {/* Image */}
            <div className="w-full h-32 border rounded-lg mb-4">
              <img
                src={imageUrl}
                alt="Card graphic"
                className="w-full h-full object-cover"
              />
            </div>
          

          {/* Description */}
          <CardDescription className="text-sm text-gray-600">
            <a
              href={url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-blue-500 hover:underline break-words"
            >
              {description}
            </a>
          </CardDescription>
        </CardContent>
        <CardFooter className="p-4  bg-gray-50">
          {/* Tags and Timestamps */}
          <div className="flex  items-start justify-between gap-2">
            {/* Tags */}
            <div className="flex flex-wrap  gap-2">
              {tags.map((tag, index) => (
                <a
                  key={index}
                  className="bg-gray-200 text-gray-800 text-xs px-2 py-1 rounded-md shadow-sm hover:cursor-pointer"
                >
                  {tag}
                </a>
              ))}
            </div>
            {/* Timestamps */}
            <div className="flex flex-wrap  gap-2">
              {timeStamps.map((timeStamp, index) => (
                <span
                  key={index}
                  className="bg-[#ffc4cc] text-xs px-2 py-1 rounded-md "
                >
                  {timeStamp}
                </span>
              ))}
            </div>
          </div>
        </CardFooter>  
        {authors[0] && ( //if authors exist, show them as well
          <div className="flex justify-end font-semibold p-2">
          By: {authors}
          </div>
        )}
      </Card>
    </div>
  );
};

export default ResultCards;
