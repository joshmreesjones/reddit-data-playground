$("#subreddit-submit").click(function() {
    var subreddit = $("#subreddit-input").val();

    if (subreddit == "") return;

    var result = $.ajax({
        url: "/similar/" + subreddit,
        cache: false,
        success: handleResponse
    });
});

var handleResponse = function(response) {
    console.log(response);
    // If the graph is new, just make the graph
    // If an existing graph is being expanded, update the graph
}
