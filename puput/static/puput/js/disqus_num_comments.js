function disqus_config() {
    this.callbacks.onNewComment = [function() { updatePostComments(); }];
}

function updatePostComments(){
    var blog_page_comments_url = $('[data-puput-page-comments-url]').data('blogPageCommentsUrl');
    $.ajaxSetup({
        beforeSend: function(xhr){
            var csrftoken = $.cookie('csrftoken');
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
    $.post(blog_page_comments_url);
}