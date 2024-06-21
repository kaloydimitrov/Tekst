const messageApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#message-app',
    data: {
        showNotification: false,
        message: ''
    },
    methods: {
        triggerNotification(newMessage) {
            if (!this.showNotification) {
                this.message = newMessage;
                this.showNotification = true;
                setTimeout(() => {
                    this.showNotification = false;
                }, 2000);
            }
        }
    }
});