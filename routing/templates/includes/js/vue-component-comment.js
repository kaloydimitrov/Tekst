Vue.component('comment', {
    props: ['comments'],
    delimiters: ['[[', ']]'],
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
        showCommentForm(commentId) {
            document.getElementById(`inputContainer${commentId}`).style.display = "block";
        },
        hideCommentForm(commentId) {
            document.getElementById(`inputContainer${commentId}`).style.display = "none";
        },
        toggleReplies(comment) {
            comment.showReplies = !comment.showReplies;
        },
        createNestedComment(comment, event) {
            const publishButton = event.target;
            const parentElement = publishButton.parentNode;
            const commentInput = parentElement.querySelector('textarea');

            if (!commentInput.value) {
                return;
            }

            publishButton.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>';

            axios.
            post(`{% url 'create_comment' %}`, {
                post: comment.post,
                content: commentInput.value,
                parent_comment: comment.id
            })
            .then(() => {
                postsApp.listComments(comment.post);
                this.hideCommentForm(comment.id);
                commentInput.value = "";
                publishButton.innerHTML = "Publish";
            })
            .catch((error) => {
                console.error(error);
                publishButton.innerHTML = "Publish";
            });
        },
        likeDislikeComment(comment) {
            if (comment.is_liked) {
                axios.
                delete(`/api/comment/${comment.id}/dislike/`)
                .then(response => {
                    console.log(response.data.message)
                    comment.likes_count -= 1;
                    comment.is_liked = false;
                })
                .catch(error => {
                    console.error(error)
                })
            } else {
                axios.
                post(`/api/comment/${comment.id}/like/`)
                .then(response => {
                    console.log(response.data.message)
                    comment.likes_count += 1;
                    comment.is_liked = true;
                })
                .catch(error => {
                    console.error(error)
                })
            }
        }
    },
    template: `
        <div class="card">
            <div class="comment card-body" v-for="comment in comments" :key="comment.id">
                <div class="d-flex justify-content-between align-items-center">
                    <small class="text-muted d-flex align-items-center">
                        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#6c757d"><path d="M480-480q-66 0-113-47t-47-113q0-66 47-113t113-47q66 0 113 47t47 113q0 66-47 113t-113 47ZM160-160v-112q0-34 17.5-62.5T224-378q62-31 126-46.5T480-440q66 0 130 15.5T736-378q29 15 46.5 43.5T800-272v112H160Zm80-80h480v-32q0-11-5.5-20T700-306q-54-27-109-40.5T480-360q-56 0-111 13.5T260-306q-9 5-14.5 14t-5.5 20v32Zm240-320q33 0 56.5-23.5T560-640q0-33-23.5-56.5T480-720q-33 0-56.5 23.5T400-640q0 33 23.5 56.5T480-560Zm0-80Zm0 400Z"/></svg>
                        &nbsp;[[ comment.user.username ]] - [[ convertIso8601Format(comment.created_at) ]]
                    </small>
                    <button v-if="comment.replies.length" class="btn btn-primary btn-sm" @click="toggleReplies(comment)">
                        <svg xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#FFFFFF">
                            <path v-if="comment.showReplies" d="M480-344 240-584l56-56 184 184 184-184 56 56-240 240Z"/>
                            <path v-else d="M480-528 296-344l-56-56 240-240 240 240-56 56-184-184Z"/>
                        </svg>
                        [[ comment.replies.length ]] reply/ies
                    </button>
                </div>
                <p class="card-text comment">[[ comment.content ]]</p>
                <div class="d-flex align-items-center likes-reply-container">
                    <span @click="likeDislikeComment(comment)" class="d-flex align-items-center justify-content-center like-button">
                        <svg v-if="comment.is_liked" xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#0b5ed7"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                        <svg v-else xmlns="http://www.w3.org/2000/svg" height="20px" viewBox="0 -960 960 960" width="20px" fill="#5f6368"><path d="M720-120H280v-520l280-280 50 50q7 7 11.5 19t4.5 23v14l-44 174h258q32 0 56 24t24 56v80q0 7-2 15t-4 15L794-168q-9 20-30 34t-44 14Zm-360-80h360l120-280v-80H480l54-220-174 174v406Zm0-406v406-406Zm-80-34v80H160v360h120v80H80v-520h200Z"/></svg>
                    </span>
                    <span id="likes" v-if="comment.likes_count > 0" class="text-muted">[[ comment.likes_count ]]</span>
                    <small><a class="link-secondary reply-link" @click="showCommentForm(comment.id)">Reply</a></small>
                </div>
                <div class="input-container" :id="'inputContainer' + comment.id">
                    <div class="d-flex align-items-start">
                        <textarea class="form-control" placeholder="Add reply..."></textarea>
                        <button class="btn btn-outline-secondary btn-sm" @click="hideCommentForm(comment.id)">Cancel</button>
                        <button class="btn btn-outline-primary btn-sm" @click="createNestedComment(comment, $event)">Publish</button>
                    </div>
                </div>
                <div v-if="comment.showReplies && comment.replies.length" id="replies">
                    <comment :comments="comment.replies" class="ml-4"></comment>
                </div>
            </div>
        </div>
    `,
});