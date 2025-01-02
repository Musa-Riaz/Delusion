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
    top_docs = []

    for doc in docs:
        doc_id = doc[0]
        hit_list = doc[1]

        this_score = min(len(hit_list), 20)   # TEXT hits, capped at 50 arbitrarily, having 50 or 100 hits does not increase relevancy much

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
                        this_score += 20
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

        top_docs.append((this_score, doc_id))

    return top_docs

def intersect(doc_lists):
    if len(doc_lists) <= 1:
        return []
    
    doc_lists = [{doc[0] : is_relevant(doc[1]) for doc in doc_list} for doc_list in doc_lists]
    intersections = [doc_lists[0]]
    
    for i in range(1, len(doc_lists)):
        this_intersection = {}
        for doc_id in doc_lists[i]:
            if doc_id in intersections[i - 1]:
                if doc_lists[i][doc_id] and intersections[i - 1][doc_id]:
                    this_intersection[doc_id] = True
                else:
                    this_intersection[doc_id] = False
        intersections.append(this_intersection)
    return intersections
        
# a hit list is considered relevant if it contains any hits other than text
def is_relevant(hit_list):
    # hit lists store hits in order title, text, url, author, tags
    # so only the first and last hits can be relevant
    return hit_list[0] % 10 != 1 or hit_list[-1] % 10 != 1

def intersection_multiplier(doc, intersections):
    # for multi-word queries, intersections contains cuwemulative intersections of all the words
    # more detail in search_util.py
    multiplier = 1
    for i in range(len(intersections) - 1, 0, -1):     # loop from last intersection (which is an intersection of all words)
        if doc[0] in intersections[i]:
            # multiplier is higher for the order of intersection the document is found in
            if intersections[i][doc[0]]:
                return (i + 1) * 100        # intersection is in title/url/authors/tags
            if multiplier == 1:
                multiplier = (i + 1) * 2    # in case a later intersection contains relevant hits
    return multiplier
