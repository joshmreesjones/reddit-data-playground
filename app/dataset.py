from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.reddit

def num_comments():
    return db.comments.count()

def subreddit_exists(subreddit):
    return db.comments.find_one({"subreddit": subreddit}) != None

def precompute():
    """Make a list of commenters in each subreddit."""

    pipeline = [
        {"$group": {"_id": "$subreddit", "authors": {"$addToSet": "$author"}}},
        {"$unwind": "$authors"},
        {"$group": {"_id": "$_id", "authors": {"$addToSet": "$authors"}, "count": {"$sum": 1}}},
        {"$match": {"count": {"$gte": 100}}},
        {"$project": {"_id": 0, "subreddit": "$_id", "authors": 1, "count": 1}},
        {"$out": "subredditcommenters"}
    ]

    db.comments.aggregate(pipeline, allowDiskUse=True)

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

    data = lambda sr: {"subreddit": sr["subreddit"],
                       "count": sr["count"],
                       "similarity": sr["similarity"]}

    return {
        "similar_to": subreddit,
        "count": len(authors),
        "recommendations": [data(subreddit) for subreddit in similarity_scores]
    }

if __name__ == "__main__":
    subreddit = raw_input("Enter a subreddit: ")
    results = similar_subreddits(subreddit)
    for sr in results["recommendations"]:
        print "\t%d\t%f\t%s" % (sr["count"], sr["similarity"], sr["subreddit"])
