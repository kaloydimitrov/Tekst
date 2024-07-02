const postsApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#app',
    data: {
        loading: false,
        next: `{% url 'get_space_posts' pk=space.pk %}?page=1`,
        noMorePosts: false,
        posts: []
    },
    methods: {
        {% include 'includes/js/vue-method-convert-iso-8601.js' %}
        {% include 'includes/js/vue-method-adjust-textarea-height.js' %}
        getMorePosts() {
            this.loading = true
            axios
            .get(this.next)
            .then((response) => {
                const posts = response.data.results.map((post) => {
                    post.comments = [];
                    post.loading_comments = false;
                    post.comment_order = '';
                    post.next_comment_page = `/api/comment/${post.id}/?page=1&order=${post.comment_order}`;
                    post.show_comments_section = false;
                    post.comments_listed = false;
                    post.comments_fullscreen = false;
                    return post;
                });
                this.posts = this.posts.concat(posts);
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
        createComment(post) {
            const commentInput = document.getElementById(`commentInput${post.id}`);
            const commentButton = document.getElementById(`commentButton${post.id}`);

            if (!commentInput.value) {
                return;
            }

            commentButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> <span class="sr-only">Loading...</span>';

            axios
            .post(`{% url 'create_comment' %}`, {
                post: post.id,
                content: commentInput.value,
            })
            .then((response) => {
                post.comments.unshift(response.data);
                commentInput.value = "";
                commentButton.innerHTML = "Publish";
            })
            .catch((error) => {
                console.error(error);
                commentButton.innerHTML = "Publish";
            });
        },
        listComments(post) {
            post.loading_comments = true;

            axios
            .get(post.next_comment_page)
            .then((response) => {
                post.comments = post.comments.concat(response.data.results);
                post.next_comment_page = response.data.next;
                post.loading_comments = false;
            })
            .catch((error) => {
                console.error(error);
                post.loading_comments = false;
            });
        },
        toggleCommentsSection(post) {
            if (!post.comments_listed) {
                post.comments_listed = true;
                this.listComments(post);
            }

            if (post.show_comments_section) {
                post.show_comments_section = false;
                const section = document.getElementById(`postCard${post.id}`);
                const offset = -16;
                const topPos = section.getBoundingClientRect().top + window.pageYOffset + offset;
                window.scrollTo({
                    top: topPos,
                    behavior: 'smooth'
                });
            } else {
                post.show_comments_section = true;
            }
        },
        toggleCommentOrder(order, post) {
            if (order === post.comment_order) {
                return;
            }

            if (order === '') {
                post.comment_order = '';
            } else if (order === 'oldest') {
                post.comment_order = 'oldest';
            } else if (order === 'top') {
                post.comment_order = 'top';
            }

            post.next_comment_page = `/api/comment/${post.id}/?page=1&order=${post.comment_order}`;
            post.comments = [];
            this.listComments(post);
        },
        toggleCommentsFullScreen(post) {
            if (post.comments_fullscreen) {
                document.body.style.overflow = '';
            } else {
                document.body.style.overflow = 'hidden';
            }
            post.comments_fullscreen = !post.comments_fullscreen;
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
                axios
                .post(`{% url 'create_reaction' %}`, {
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
        handleCommentsScroll(post, event) {
            const element = event.target;

            if (post.next_comment_page && !post.loading_comments && (element.scrollTop + element.clientHeight >= element.scrollHeight - 40)) {
                this.listComments(post);
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