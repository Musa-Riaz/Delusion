from sortedcontainers import SortedList

# given the documents of 1 word, ranks them based on word hits
def rank_docs(docs, intersections):
    # any hits other than TEXT are referred to as special hits
    # TITLE = 0
    # TEXT = 1
    # URL = 2
    # AUTHORS = 3
    # TAGS = 5

    # prevents special hit bonuses from stacking up
    # this decision was made as many articles contain tags such as 'Apple', 'Apple Watch', 'Apple Seminar' and so on
    # not necessarily adding to the relevancy of the document
    added = [False for i in range(6)]
    top_docs = SortedList()     # stores the top documents in a sorted manner efficiently using a binary tree

    for doc in docs:
        doc_id = doc[0]
        hit_list = doc[1]

        this_score = min(len(hit_list), 50)   # TEXT hits, capped at 50 arbitrarily, having 50 or 100 hits does not increase relevancy much

        multiplier = intersection_multiplier(doc, intersections)
        this_score = this_score if multiplier == 1 else this_score + 10

        # smart checking of hits
        # by design, hits are stored in the indexes with TITLE first, then all TEXT hits, then URL, AUTHOR, TAGS
        i = 0
        step = 1    # initially, go forward through the hit list
        while i >= 0 and i < len(hit_list):
            hit = hit_list[i]

            # weightages decided arbitrarily
            match hit % 10: 
                case 0:
                    if not added[0]:
                        this_score += 50
                        added[0] = True
                case 2:
                    if not added[2]:
                        this_score += 30
                        added[2] = True
                case 3:
                    if not added[3]:
                        this_score += 40
                        added[3] = True
                case 5:
                    if not added[5]:
                        this_score += 30
                        added[5] = True
            
            # if a TEXT hit is encountered, all TITLE hits have been processed
            # skip to the last hit
            if hit % 10 == 1:
                if step == 1:
                    i = len(hit_list) - 1
                    step = -1       # iterate backwards now
                else:
                    # iterating backwards, reached a TEXT hit, meaning URL, TAGS, AUTHOR hits have been processed too
                    break
            else:
                i += step

        this_score *= multiplier

        # SortedList() stores in ascending order by default
        # storing negative scores to simulate descending order
        top_docs.add((-1 * this_score, doc_id))

    return top_docs


def intersection_multiplier(doc, intersections):
    # for multi-word queries, intersections contains cuwemulative intersections of all the words
    # more detail in search_util.py
    for i in range(len(intersections) - 1, 0, -1):     # loop from last intersection (which is an intersection of all words)
        if doc[0] in intersections[i]:
            # multiplier is higher for the order of intersection the document is found in
            if intersections[i][doc[0]]:
                return (i + 1) * 100        # intersection is in title/url/authors/tags
            return (i + 1) * 2
    return 1