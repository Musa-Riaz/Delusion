import React from "react";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Star } from "lucide-react";


const ResultCards = ({
  title,
  description,
  url,
  imageUrl,
  tags,
  timeStamps,
  authors
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
                src={imageUrl !== "" ? imageUrl : "https://miro.medium.com/v2/resize:fit:1200/1*oXT1gXRoUxIs8dkDB7wUDQ.png"}
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
              dangerouslySetInnerHTML={{ __html: description }}
            />
          </CardDescription>
        </CardContent>
        <CardFooter className="p-4  bg-gray-50">
          {/* Tags and Timestamps */}
          <div className="flex  items-end justify-between gap-2">
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
                  className="bg-[#ffc4cc] w-20 text-xs px-2 py-1 rounded-md "
                >
                  {timeStamp}
                </span>
              ))}
            </div>
          </div>
        </CardFooter>  
        {authors ?  ( //if authors exist, show them as well
          <div className="flex justify-end gap-1 font-semibold p-2">
          By: 
            <span >
              {authors}
            </span>
          </div>
        ) : (<p className="flex justify-end gap-1 font-semibold p-2">By: No author, just vibes</p>)}
      </Card>
    </div>
  );
};

export default ResultCards;
