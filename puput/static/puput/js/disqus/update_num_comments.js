function disqus_config() {
    this.callbacks.onNewComment = [function() { updateEntryComments(); }];
}

function updateEntryComments() {
    var entryPageUpdateCommentsUrl = $('[data-entry-page-update-comments-url]').data('entryPageUpdateCommentsUrl');
    $.ajaxSetup({
        beforeSend: function(xhr) {
            var csrftoken = Cookies.get('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    $.post(entryPageUpdateCommentsUrl);
}