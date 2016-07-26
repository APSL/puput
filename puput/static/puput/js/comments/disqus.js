function disqus_config() {
    this.callbacks.onNewComment = [function() { updateEntryComments(); }];
}