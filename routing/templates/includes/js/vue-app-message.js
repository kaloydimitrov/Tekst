const messageApp = new Vue({
    delimiters: ['[[', ']]'],
    el: '#message-app',
    data: {
        showNotification: false,
        message: ''
    },
    methods: {
        triggerNotification(message) {
            this.message = message;

            this.showNotification = true;
            setTimeout(() => {
                this.showNotification = false;
            }, 2000);
        }
    }
});