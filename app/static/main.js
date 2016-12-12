var handleSubmit = function() {
    var subreddit = $("#subreddit-input").val();

    if (subreddit == "") return;

    $(".loader").show();

    var result = $.ajax({
        url: "/similar/" + subreddit,
        cache: false,
        success: handleResponse
    });
};

var handleResponse = function(response) {
    $(".loader").hide();

    console.log(response);
}

$("#subreddit-submit").click(handleSubmit);
