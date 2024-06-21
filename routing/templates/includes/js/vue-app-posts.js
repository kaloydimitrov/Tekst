const postsApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        loading: false,
        next: `{% url 'get_space_posts' pk=space.pk %}?page=1`,
        noMorePosts: false,
        posts: [],
        comments: {},
    },
    methods: {
        {% include 'includes/js/vue-method-convert-iso-8601.js' %}
        {% include 'includes/js/vue-method-adjust-textarea-height.js' %}
        organizeComments(commentsData) {
            const commentsMap = {};
            const nestedComments = [];

            commentsData.forEach(comment => {
                comment.showReplies = true;
                comment.replies = [];
                commentsMap[comment.id] = comment;
            });

            commentsData.forEach(comment => {
                if (comment.parent_comment !== null) {
                    commentsMap[comment.parent_comment].replies.push(comment);
                } else {
                    nestedComments.push(comment);
                }
            });

            return nestedComments;
        },
        getMorePosts() {
            this.loading = true
            axios.
            get(this.next)
            .then((response) => {
                this.posts = this.posts.concat(response.data.results);
                this.next = response.data.next;
                if (!this.next) {
                    this.noMorePosts = true;
                }
                this.loading = false;
            })
            .catch(() => {
                this.noMorePosts = true;
                this.loading = false;
            });
        },
        createComment(postId) {
            const commentInput = document.getElementById(`commentInput${postId}`);
            const commentButton = document.getElementById(`commentButton${postId}`);

            if (!commentInput.value) {
                return;
            }

            commentButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> <span class="sr-only">Loading...</span>';

            axios.
            post(`{% url 'create_comment' %}`, {
                post: postId,
                content: commentInput.value,
            })
            .then(() => {
                this.listComments(postId);
                commentInput.value = "";
                commentButton.innerHTML = "Publish";
            })
            .catch((error) => {
                console.error(error);
                commentButton.innerHTML = "Publish";
            });
        },
        listComments(postId) {
            const spinner = document.getElementById(`loadingContainer${postId}`);

            axios.
            get(`/api/comment/${postId}/`)
            .then((response) => {
                this.$set(this.comments, postId, this.organizeComments(response.data));
                spinner.remove();
            })
            .catch((error) => {
                console.error(error);
                spinner.remove();
            });
        },
        toggleReaction(reaction, post) {
            if (reaction.is_reacted) {
                axios.delete(`{% url 'delete_reaction' %}`, {
                    data: {
                        post: post.id,
                        reaction_type: reaction.id,
                    }
                })
                .then(() => {
                    reaction.is_reacted = false;
                    messageApp.triggerNotification('Reaction removed');
                })
                .catch((error) => {
                    console.error(error.response.data);
                });
            } else {
                axios.
                post(`{% url 'create_reaction' %}`, {
                    post: post.id,
                    reaction_type: reaction.id,
                })
                .then(() => {
                    post.reactions.forEach((reaction) => reaction.is_reacted = false);
                    reaction.is_reacted = true;
                    messageApp.triggerNotification('Reacted successfully');
                })
                .catch((error) => {
                    console.error(error.response.data);
                });
            }
        },
        handleScroll() {
            if (!this.noMorePosts && !this.loading && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
                this.getMorePosts();
            }
        },
    },
    mounted() {
        this.getMorePosts();
        window.addEventListener('scroll', this.handleScroll);
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.handleScroll);
    },
});