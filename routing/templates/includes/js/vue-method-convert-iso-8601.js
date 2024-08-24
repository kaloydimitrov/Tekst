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

    return date.toLocaleString('BG', options);
},