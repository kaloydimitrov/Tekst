const postsApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        page: 1,
        loading: false,
        noMorePosts: false,
        posts: [],
        comments: {},
    },
    methods: {
        convertIso8601Format(isoTimestamp) {
            const date = new Date(isoTimestamp);

            const options = {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: 'numeric',
                minute: 'numeric',
                second: 'numeric',
            };

            return date.toLocaleString('en-US', options);
        },
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
            if (!this.noMorePosts && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
                this.getMorePosts();
            }
        },
        getMorePosts() {
            this.loading = true
            axios.
            get(`{% url 'get_space_posts' pk=space.pk %}?page=${this.page}`)
            .then((response) => {
                this.posts = this.posts.concat(response.data.results);
                this.page += 1;
                this.loading = false
            })
            .catch(() => {
                this.noMorePosts = true;
                this.loading = false
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