const toolbarOptions = [
    [{ 'header': [1, 2, 3, false] }],
    ['bold', 'italic', 'underline', 'strike'],
    [{ 'align': [] }],
    [{ 'color': [] }],
    ['clean'],
];

const quill = new Quill('#editor', {
    theme: 'snow',
    modules: {
        toolbar: toolbarOptions
    }
});

if (place === 'space') {
    quill.root.dataset.placeholder = 'Въведи описание';
} else if (place === 'post') {
    quill.root.dataset.placeholder = 'Основен текст*';
}

quill.on('text-change', () => {
    if (place === 'space') {
        this.descriptionInput = quill.root.innerHTML;
    } else if (place === 'post') {
        this.content = quill.root.innerHTML;
    }
});