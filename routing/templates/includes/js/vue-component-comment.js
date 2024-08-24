Vue.component('comment', {
    props: ['comments'],
    delimiters: ['[[', ']]'],
    methods: {
        {% include 'includes/js/vue-method-convert-iso-8601.js' %}
        {% include 'includes/js/vue-method-adjust-textarea-height.js' %}
        showCommentForm(commentId) {
            document.getElementById(`inputContainer${commentId}`).style.display = "block";
        },
        hideCommentForm(commentId) {
            document.getElementById(`inputContainer${commentId}`).style.display = "none";
        },
        switchEditComment(comment) {
            Vue.set(comment, 'edit_mode', true);
        },
        toggleReplies(comment) {
            comment.show_replies = !comment.show_replies;
        },
        createNestedComment(comment, event) {
            const publishButton = event.target;
            const parentElement = publishButton.parentNode.parentNode;
            const commentInput = parentElement.querySelector('textarea');

            if (!commentInput.value) {
                return;
            }

            publishButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            axios
            .post(`{% url 'create_comment' %}`, {
                post: comment.post,
                content: commentInput.value,
                parent_comment: comment.id
            })
            .then((response) => {
                comment.replies.unshift(response.data);
                comment.show_replies = true;
                this.hideCommentForm(comment.id);
                commentInput.value = "";
                publishButton.innerHTML = "Publish";
                messageApp.triggerNotification('Replied successfully');
            })
            .catch((error) => {
                console.error(error);
                publishButton.innerHTML = "Publish";
            });
        },
        editComment(comment) {
            const contentValue = this.$refs['editCommentField' + comment.id][0].value;
            if (!contentValue) { return; }

            axios
            .put(`/api/comment/${comment.id}/update/`, {
                post: comment.post,
                content: contentValue,
                parent_comment: comment.parent_comment
            })
            .then(() => {
                comment.content = contentValue;
                comment.edit_mode = false;
                messageApp.triggerNotification('Comment edited');
            })
            .catch((error) => {
                console.error(error);
            });
        },
        handleEditCommentField(event, comment) {
            const saveButton = this.$refs['saveCommentButton' + comment.id][0];
            if (comment.content !== event.target.value) {
                saveButton.classList.replace('half-opacity', 'opacity-100');
            } else  {
                saveButton.classList.replace('opacity-100', 'half-opacity');
            }

            this.adjustTextAreaHeight(event);
        },
        deleteComment(comment) {
            axios
            .delete(`/api/comment/${comment.id}/delete/`)
            .then(() => {
                {% if in_post_details %}
                this.deleteCommentRecursive(this.comments, comment.id);
                {% else %}
                let post = postsApp.posts.find(p => p.id === comment.post);
                this.deleteCommentRecursive(post.comments, comment.id);
                {% endif %}
                messageApp.triggerNotification('Comment deleted');
            })
            .catch((error) => {
                console.error(error);
            });
        },
        deleteCommentRecursive(comments, commentId) {
            let index = comments.findIndex(c => c.id === commentId);

            if (index !== -1) {
                comments.splice(index, 1);
            } else {
                comments.forEach(comment => {
                    this.deleteCommentRecursive(comment.replies, commentId);
                });
            }
        },
        likeDislikeComment(comment) {
            if (comment.is_liked) {
                axios
                .delete(`/api/comment/${comment.id}/dislike/`)
                .then(response => {
                    comment.likes_count -= 1;
                    comment.is_liked = false;
                    messageApp.triggerNotification(response.data.message);
                })
                .catch(error => {
                    console.error(error)
                })
            } else {
                axios
                .post(`/api/comment/${comment.id}/like/`)
                .then(response => {
                    comment.likes_count += 1;
                    comment.is_liked = true;
                    messageApp.triggerNotification(response.data.message);
                })
                .catch(error => {
                    console.error(error)
                })
            }
        }
    },
    template: `
        <div class="card">
            <div :class="['comment', 'card-body', {'linked-comment': comment.is_linked}]" v-for="comment in comments" :key="comment.id" v-if="!comment.deleted && !(!comment.is_linked && comment.id === {% if request.GET.comment_link %}{{ request.GET.comment_link }}{% else %}none{% endif %})" style="min-width: 400px;">
                <div v-if="comment.is_linked" class="linked-comment-alert">
                    <svg xmlns="http://www.w3.org/2000/svg" height="22px" viewBox="0 -960 960 960" width="22px" fill="#000000"><path d="M432.31-298.46H281.54q-75.34 0-128.44-53.1Q100-404.65 100-479.98q0-75.33 53.1-128.44 53.1-53.12 128.44-53.12h150.77v60H281.54q-50.39 0-85.96 35.58Q160-530.38 160-480q0 50.38 35.58 85.96 35.57 35.58 85.96 35.58h150.77v60ZM330-450v-60h300v60H330Zm197.69 151.54v-60h150.77q50.39 0 85.96-35.58Q800-429.62 800-480q0-50.38-35.58-85.96-35.57-35.58-85.96-35.58H527.69v-60h150.77q75.34 0 128.44 53.1Q860-555.35 860-480.02q0 75.33-53.1 128.44-53.1 53.12-128.44 53.12H527.69Z"/></svg>
                    <span>Връзка с коментар</span>
                    <span v-if="comment.parent_comment">&middot;</span>
                    <a v-if="comment.parent_comment" :href="'/post/{{ post.slug }}/?comment_link=' + comment.parent_comment">Това е отговор на този коментар</a>
                </div>
                <div class="d-flex justify-content-between">
                    <small class="text-muted d-flex gap-1 align-items-center">
                        <a class="d-flex align-items-end" :href="'/user/profile/' + comment.user.slug">
                            <svg xmlns="http://www.w3.org/2000/svg" height="19px" viewBox="0 -960 960 960" width="19px" fill="#0d6efd"><path d="M480-504.62q-49.5 0-84.75-35.25T360-624.62q0-49.5 35.25-84.75T480-744.62q49.5 0 84.75 35.25T600-624.62q0 49.5-35.25 84.75T480-504.62ZM200-215.38v-65.85q0-24.77 14.42-46.35 14.43-21.57 38.81-33.5 56.62-27.15 113.31-40.73 56.69-13.57 113.46-13.57 56.77 0 113.46 13.57 56.69 13.58 113.31 40.73 24.38 11.93 38.81 33.5Q760-306 760-281.23v65.85H200Zm40-40h480v-25.85q0-13.31-8.58-25-8.57-11.69-23.73-19.77-49.38-23.92-101.83-36.65-52.45-12.73-105.86-12.73t-105.86 12.73Q321.69-349.92 272.31-326q-15.16 8.08-23.73 19.77-8.58 11.69-8.58 25v25.85Zm240-289.24q33 0 56.5-23.5t23.5-56.5q0-33-23.5-56.5t-56.5-23.5q-33 0-56.5 23.5t-23.5 56.5q0 33 23.5 56.5t56.5 23.5Zm0-80Zm0 369.24Z"/></svg>
                            <span>[[ comment.user.username ]]</span>
                        </a>
                        <span>-</span>
                        <span>[[ convertIso8601Format(comment.created_at) ]]</span>
                    </small>
                    <div class="dropdown">
                        <div class="comment-options d-flex align-items-center justify-content-center" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5f6368"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>
                        </div>
                        <ul v-if="comment.user.id === {{ request.user.pk }}" class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <li class="dropdown-item cursor-pointer" @click="switchEditComment(comment)">Редактирай</li>
                            <li class="dropdown-item cursor-pointer" @click="deleteComment(comment)">Изтрий</li>
                        </ul>
                        <ul v-else class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <li class="dropdown-item cursor-pointer">Докладвай</li>
                        </ul>
                    </div>
                </div>
                <p v-if="!comment.edit_mode" class="card-text comment">[[ comment.content ]]</p>
                <div v-else>
                    <textarea class="form-control comment-textarea" :ref="'editCommentField' + comment.id" @input="handleEditCommentField($event, comment)">[[ comment.content ]]</textarea>
                    <div class="mt-2 mb-2 gap-1 d-flex">
                        <button class="btn btn-outline-secondary btn-sm" @click="comment.edit_mode = false">Откажи</button>
                        <button class="btn btn-outline-primary btn-sm half-opacity" :ref="'saveCommentButton' + comment.id" @click="editComment(comment)">Запази</button>
                    </div>
                </div>
                <div class="likes-reply-container mb-1">
                    <span @click="likeDislikeComment(comment)" class="d-flex align-items-center justify-content-center like-button">
                        <svg v-if="comment.is_liked" xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#0b5ed7"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5f6368"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                    </span>
                    <span id="likes" v-if="comment.likes_count > 0" class="text-muted">[[ comment.likes_count ]]</span>
                    <div class="vr mx-1"></div>
                    <small><a class="link-secondary reply-link" @click="showCommentForm(comment.id)">Отговори</a></small>
                </div>
                <button v-if="comment.replies.length" :class="['answer-button', 'text-muted', 'small', 'd-flex', 'align-items-center', {'half-opacity': comment.show_replies}]" @click="toggleReplies(comment)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6c757d">
                        <path v-if="comment.show_replies" d="M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"/>
                        <path v-else d="M480-528 296-344l-56-56 240-240 240 240-56 56-184-184Z"/>
                    </svg>
                    &nbsp;[[ comment.replies.length ]]&nbsp;
                    <span v-if="comment.replies.length === 1">отговор</span>
                    <span v-else>отговора</span>
                </button>
                <div class="input-container" :id="'inputContainer' + comment.id">
                    <div class="d-flex flex-column">
                        <textarea class="form-control comment-textarea" placeholder="Добави отговор" @input="adjustTextAreaHeight"></textarea>
                        <div class="mt-2 gap-1 d-flex">
                            <button class="btn btn-outline-secondary btn-sm" @click="hideCommentForm(comment.id)">Откажи</button>
                            <button class="btn btn-outline-primary btn-sm" @click="createNestedComment(comment, $event)">Публикувай</button>
                        </div>
                    </div>
                </div>
                <div v-if="comment.replies.length && comment.show_replies" id="replies">
                    <comment :comments="comment.replies" class="ml-4"></comment>
                </div>
            </div>
        </div>
    `,
});