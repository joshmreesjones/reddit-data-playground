from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.reddit

# Note: the data must be imported to a local MongoDB database for this code to work.
comments100      = db.comments100
comments100000   = db.comments100000
comments1000000  = db.comments1000000
comments10000000 = db.comments10000000
commentsall      = db.commentsall

#db.comments = comments10000000

def similar_subreddits(subreddit):
    # Get the authors of this subreddit.
    result = db.subredditcommenters.find({"subreddit": subreddit})

    if result.count() == 0: return None

    authors = result.next()["authors"]

    # Compute similarity scores for each other subreddit.
    similarity_scores = db.subredditcommenters.aggregate([
        {"$project": {
            "subreddit": True,
            "count": True,
            "similarity": {
                "$divide": [
                    {"$size": {"$setIntersection": [authors, "$authors"]}},
                    "$count"
                ]
             }
        }},
        {"$match": {
            "$and": [
                {"similarity": {"$ne": 1}},
                {"similarity": {"$ne": 0}}
            ]
        }},
        {"$sort": {"similarity": -1}},
        {"$limit": 15}
    ])

    return [
        {
            "subreddit": subreddit["subreddit"],
            "count": subreddit["count"],
            "similarity": subreddit["similarity"]
        } for subreddit in similarity_scores
    ]


def precompute():
    # Make a list of commenters in each subreddit.
    commenters_per_subreddit = db.comments.aggregate([
        {"$group": {"_id": "$subreddit", "authors": {"$addToSet": "$author"}}},
        {"$unwind": "$authors"},
        {"$group": {"_id": "$_id", "authors": {"$addToSet": "$authors"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": 100}}},
        {"$project": {"_id": 0, "subreddit": "$_id", "authors": 1, "count": 1}},
        {"$out": "subredditcommenters"}
    ],
    {
        "allowDiskUse": True
    })

if __name__ == "__main__":
    subreddit = raw_input("Enter a subreddit: ")
    similar = similar_subreddits(subreddit)
    if similar:
        print "Subreddits similar to %s:" % subreddit
        for sr in similar:
            print "\t%d\t%f\t%s" % (sr["count"], sr["similarity"], sr["subreddit"])
    else:
        print "There are no comments in the dataset for %s." % subreddit
