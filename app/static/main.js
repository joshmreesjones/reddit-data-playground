var handleSubmit = function() {
    var subreddit = $("#subreddit-input").val();

    if (subreddit == "") return;

    $(".loader").show();

    var result = $.ajax({
        url: "/similar/" + subreddit,
        success: handleResponse
    });
};

var handleResponse = function(response) {
    $(".loader").hide();

    var graph = {"nodes": [], "links": []};

    // Add the central node (the input subreddit)
    graph["nodes"].push({"id": response["similar_to"], "value": response["count"]});

    // Add other nodes and links
    var subreddit = response["similar_to"];
    var recommendations = response["recommendations"];
    for (var index in recommendations) {
        recommendation = recommendations[index];

        graph["nodes"].push({"id": recommendation["subreddit"], "value": recommendation["count"]});
        graph["links"].push({"source": subreddit, "target": recommendation["subreddit"], "value": recommendation["similarity"]});
    }

    updateGraph(graph);
}

$("#subreddit-submit").click(handleSubmit);
