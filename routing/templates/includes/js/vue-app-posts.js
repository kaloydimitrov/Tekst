const postsApp = new Vue({
    el: '#app',
    delimiters: ['[[', ']]'],
    components: {
        {% if not in_space_details %}vuejsDatepicker{% endif %}
    },
    data: {
        {% if not in_space_details %}bg: vdp_translation_bg.js,{% endif %}
        is_authenticated: {% if request.user.is_authenticated %}true{% else %}false{% endif %},
        loading: false,
        next: `${postsURL}?page=1`,
        posts: [],

        // Filters
        showFilters: false,
        filter: {% if not in_space_details %}'trending'{% else %}'newest'{% endif %},
        fromDate: null,
        toDate: null,
    },
    methods: {
        {% include 'includes/js/vue-method-convert-iso-8601.js' %}
        {% include 'includes/js/vue-method-adjust-textarea-height.js' %}
        navigateToSpace(slug) {
            window.location.href = `/space/${slug}/`;
        },
        navigateToPost(slug) {
            window.location.href = `/post/${slug}/`;
        },
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
                this.loading = false;
            })
            .catch(() => {
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
                messageApp.triggerNotification('Comment created');
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
                document.body.style.overflow = 'scroll';
            } else {
                post.show_comments_section = true;
                document.body.style.overflow = 'hidden';
            }
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
        switchCommentsOrder(order, post) {
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
        switchPostsFilter(filter, ignoreFilterCheck = false) {
            if (filter === this.filter && !ignoreFilterCheck) {
                return;
            }

            if (this.fromDate || this.toDate) {
                this.next = `${postsURL}?page=1&filter=${filter}&date=${this.reformatDate(this.fromDate)}|${this.reformatDate(this.toDate)}`;
            } else {
                this.next = `${postsURL}?page=1&filter=${filter}`;
            }
            this.posts = [];
            this.getMorePosts();
            this.filter = filter;
        },
        reformatDate(date) {
            if (!date) {
                return '';
            }

            const dateObj = new Date(date);
            const year = dateObj.getFullYear();
            const month = dateObj.getMonth() + 1;
            const day = dateObj.getDate();

            return `${year},${month},${day}`;
        },
        handleCommentsScroll(post, event) {
            const element = event.target;

            if (post.next_comment_page && !post.loading_comments && (element.scrollTop + element.clientHeight >= element.scrollHeight - 40)) {
                this.listComments(post);
            }
        },
        handleScroll() {
            if (this.next && !this.loading && (window.innerHeight + window.scrollY) >= document.body.offsetHeight - 10) {
                this.getMorePosts();
            }
        },
    },
    watch: {
        fromDate(newValue) {
            this.switchPostsFilter(this.filter, true)
        },
        toDate(newValue) {
            this.switchPostsFilter(this.filter, true)
        }
    },
    mounted() {
        this.getMorePosts();
        window.addEventListener('scroll', this.handleScroll);

        document.body.style.overflow = 'scroll';
        document.body.style.overflowX = 'hidden';
    },
    beforeDestroy() {
        window.removeEventListener('scroll', this.handleScroll);
    },
});