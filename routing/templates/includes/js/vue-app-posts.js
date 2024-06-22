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
            axios.
            get(this.next)
            .then((response) => {
                const posts = response.data.results.map((post) => {
                    post.comments = [];
                    post.loading_comments = true;
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

            axios.
            post(`{% url 'create_comment' %}`, {
                post: post.id,
                content: commentInput.value,
            })
            .then(() => {
                this.listComments(post, false);
                commentInput.value = "";
                commentButton.innerHTML = "Publish";
            })
            .catch((error) => {
                console.error(error);
                commentButton.innerHTML = "Publish";
            });
        },
        listComments(post, goToSection = true) {
            if (goToSection) {
                const section = document.getElementById(`stickyHeader${post.id}`);
                section.scrollIntoView({ behavior: 'smooth' });
            }

            axios.
            get(`/api/comment/${post.id}/`)
            .then((response) => {
                post.comments = response.data;
                post.loading_comments = false;
            })
            .catch((error) => {
                console.error(error);
                post.loading_comments = false;
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