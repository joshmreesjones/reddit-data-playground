$("#subreddit-submit").click(function() {
    var subreddit = $("#subreddit-input").val();
    similar = similarSubreddits(subreddit);
});

var similarSubreddits = function(subreddit) {
    console.log("Finding some similar subreddits to " + subreddit);
    return null;
}
