import React from "react";
import ResultCards from "@/Components/ResultCards";
import { Search } from "lucide-react";
import { useState } from "react";
import {
  Pagination,
  PaginationContent,
  PaginationEllipsis,
  PaginationItem,
  PaginationLink,
  PaginationNext,
  PaginationPrevious,
} from "@/components/ui/pagination";
const tempData = [
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
  {
    title: "Mental Note Vol. 24",
    description:
      "This is a descrription of the article that is being sent from the results page",
    url: "https://medium.com/invisible-illness/mental-note-vol-24-969b6a42443f",
    imageUrl:
      "https://miro.medium.com/v2/resize:fit:828/format:webp/0*7oicLRRCDEyuEdGl",
    tags: ["Mental Health", "Health", "Psychology", "Science", "Neuroscience"],
    timeStamps: ["timestamp1", "timestamp2"],
  },
];
// This is the ResultsPage component that will be rendered when the user searches for something
const ResultsPage = () => {
  const [query, setQuery] = useState("");
  return (
    <div className="bg-[#ffecd4] ">
      <div className="flex justify-center items-center flex-col gap-6 p-10">
        <div className="w-[40vw] h-[6vh] flex rounded-lg border-4  border-black ">
          <input
            type="text"
            placeholder="Type Anything"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="bg-[#ffecd4] w-full text-xl placeholder-black placeholder:text-xl p-3 focus:outline-none"
          />
          <span className="flex p-5 border-l-4 border-black items-center hover:shadow-2xl transition hover:cursor-pointer">
            <Search />
          </span>
        </div>
        <h1 className="text-5xl font-semibold">Results</h1>
      </div>
      <div className="flex flex-wrap justify-between p-5">
        {tempData.map((data, index) => (
          <ResultCards
            key={index}
            title={data.title}
            description={data.description}
            url={data.url}
            image={data.imageUrl}
            tags={data.tags}
            timeStamps={data.timeStamps}
          />
        ))}
      </div>

      <div className="p-8  flex justify-center items-center border-black">
        <div>
        <Pagination >
          <PaginationContent >
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
    </div>
  );
};

export default ResultsPage;
