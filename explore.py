from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.reddit

comments100      = db.comments100
comments100000   = db.comments100000
comments1000000  = db.comments1000000
comments10000000 = db.comments10000000
commentsall      = db.commentsall

db.comments = comments1000000

def exploratory_stats():
    # How many comments are there?
    count = db.comments.count()
    print "There are %d comments." % count

    # How many subreddits are there?
    subreddits = db.comments.distinct("subreddit")
    print "There are %d subreddits." % len(subreddits)

    # How many authors are there?
    users = db.comments.distinct("author")
    print "There are %d authors." % len(users)

    # How many upvotes have been cast?
    upvotes_cursor = db.comments.aggregate([{"$group": {"_id": None, "total": {"$sum": "$ups"}}}])
    upvotes = upvotes_cursor.next()["total"]
    print "%s upvotes have been cast." % upvotes

    # How many comments are in each subreddit?
    comment_counts = db.comments.aggregate([
        {"$group": {"_id": "$subreddit", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ])
    print "The subreddits with the most comments are:"
    for comment_count in comment_counts:
        print "\t%d\t/r/%s" % (comment_count["total"], comment_count["_id"])

    # How many upvotes have been cast in each subreddit?
    upvote_counts = db.comments.aggregate([
        {"$group": {"_id": "$subreddit", "total": {"$sum": "$ups"}}},
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ])
    print "The subreddits with the most upvotes are:"
    for upvote_count in upvote_counts:
        print "\t%d\t/r/%s" % (upvote_count["total"], upvote_count["_id"])

    # Which subreddits have the most commenters?
    commenters_in_askreddit = db.comments.aggregate([
        {"$match": {"subreddit": "AskReddit"}},
        {"$group": {"_id": "$author", "total": {"$sum": 1}}},
        {"$sort": {"total": -1}},
        {"$limit": 10}
    ])
    print "The commenters who commented the most in this subreddit are:"
    for commenter in commenters_in_askreddit:
        print "\t%d\t%s" % (commenter["total"], commenter["_id"])

    # Rank the subreddits by average comment length.
    # Rank the subreddits by average sentence length.
    # Rank the subreddits by average number of upvotes per comment
    # Rank commenters by number of comments they've submitted. What percentage of comments are created by the top X% of these commenters?
    # What are the most common comments?
    # What users have the highest average number of upvotes per comment?
    # Make a list of words and their frequencies (also know how many total words there are in the corpus).
    # If we build tree structures of all comments using "parent_id", what is the average depth and size of the tree?
    # How many comments are usually posted in each hour of the day?
    # Collect lots of data about each subreddit and use a KNN classifier to cluster subreddits. This is the basis of the recommnder system.
    # How does "ups" correspond with a sentiment analysis? (this might be Karl's analysis - check before doing this)
    # Use a bag of words model to compute similarity between two subreddits
    pass

if __name__ == "__main__":
    exploratory_stats()
