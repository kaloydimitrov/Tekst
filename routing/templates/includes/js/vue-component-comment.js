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
                let post = postsApp.posts.find(p => p.id === comment.post);
                this.deleteCommentRecursive(post.comments, comment.id);
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
            <div class="comment card-body" v-for="comment in comments" :key="comment.id" v-if="!comment.deleted">
                <div class="d-flex justify-content-between">
                    <small class="text-muted d-flex align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6c757d"><path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Zm80-80h480v-32q0-11-5.5-20T700-306q-54-27-109-40.5T480-360q-56 0-111 13.5T260-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T560-640q0-33-23.5-56.5T480-720q-33 0-56.5 23.5T400-640q0 33 23.5 56.5T480-560Zm0-80Zm0 400Z"/></svg>
                        &nbsp;[[ comment.user.username ]] - [[ convertIso8601Format(comment.created_at) ]]
                    </small>
                    <div class="dropdown">
                        <div class="comment-options d-flex align-items-center justify-content-center" type="button" id="dropdownMenuButton" data-bs-toggle="dropdown" aria-expanded="false">
                            <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#5f6368"><path d="M480-160q-33 0-56.5-23.5T400-240q0-33 23.5-56.5T480-320q33 0 56.5 23.5T560-240q0 33-23.5 56.5T480-160Zm0-240q-33 0-56.5-23.5T400-480q0-33 23.5-56.5T480-560q33 0 56.5 23.5T560-480q0 33-23.5 56.5T480-400Zm0-240q-33 0-56.5-23.5T400-720q0-33 23.5-56.5T480-800q33 0 56.5 23.5T560-720q0 33-23.5 56.5T480-640Z"/></svg>
                        </div>
                        <ul v-if="comment.user.id === {{ request.user.pk }}" class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <li class="dropdown-item" @click="switchEditComment(comment)">Edit</li>
                            <li class="dropdown-item" @click="deleteComment(comment)">Delete</li>
                        </ul>
                        <ul v-else class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                            <li class="dropdown-item">Report</li>
                        </ul>
                    </div>
                </div>
                <p v-if="!comment.edit_mode" class="card-text comment">[[ comment.content ]]</p>
                <div v-else>
                    <textarea class="form-control comment-textarea" :ref="'editCommentField' + comment.id" @input="handleEditCommentField($event, comment)">[[ comment.content ]]</textarea>
                    <div class="mt-2 mb-2 gap-1 d-flex">
                        <button class="btn btn-outline-secondary btn-sm" @click="comment.edit_mode = false">Cancel</button>
                        <button class="btn btn-outline-primary btn-sm half-opacity" :ref="'saveCommentButton' + comment.id" @click="editComment(comment)">Save</button>
                    </div>
                </div>
                <div class="likes-reply-container mb-1">
                    <span @click="likeDislikeComment(comment)" class="d-flex align-items-center justify-content-center like-button">
                        <svg v-if="comment.is_liked" xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#0b5ed7"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5f6368"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                    </span>
                    <span id="likes" v-if="comment.likes_count > 0" class="text-muted">[[ comment.likes_count ]]</span>
                    <div class="vr mx-1"></div>
                    <small><a class="link-secondary reply-link" @click="showCommentForm(comment.id)">Reply</a></small>
                </div>
                <button v-if="comment.replies.length" :class="['answer-button', 'text-muted', 'small', 'd-flex', 'align-items-center', {'half-opacity': comment.show_replies}]" @click="toggleReplies(comment)">
                    <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6c757d">
                        <path v-if="comment.show_replies" d="M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"/>
                        <path v-else d="M480-528 296-344l-56-56 240-240 240 240-56 56-184-184Z"/>
                    </svg>
                    &nbsp;[[ comment.replies.length ]]&nbsp;
                    <span v-if="comment.replies.length === 1">answer</span>
                    <span v-else>answers</span>
                </button>
                <div class="input-container" :id="'inputContainer' + comment.id">
                    <div class="d-flex flex-column">
                        <textarea class="form-control comment-textarea" placeholder="Add reply..." @input="adjustTextAreaHeight"></textarea>
                        <div class="mt-2 gap-1 d-flex">
                            <button class="btn btn-outline-secondary btn-sm" @click="hideCommentForm(comment.id)">Cancel</button>
                            <button class="btn btn-outline-primary btn-sm" @click="createNestedComment(comment, $event)">Publish</button>
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