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
        handleScroll() {
            if (!this.noMorePosts && !this.loading && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
                this.getMorePosts();
            }
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
            const spinner= document.querySelector(`#loadingContainer${postId} .spinner-border`);

            axios.
            get(`/api/comment/${postId}/`)
            .then((response) => {
                this.$set(this.comments, postId, this.organizeComments(response.data));
                spinner.style.display = "none";
            })
            .catch((error) => {
                console.error(error);
                spinner.style.display = "none";
            });
        }
    },
    mounted() {
        this.getMorePosts();
        window.addEventListener('scroll', this.handleScroll);
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.handleScroll);
    },
});