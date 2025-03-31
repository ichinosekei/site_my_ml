document.getElementById('chat-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const inputField = document.getElementById('user-input');
    const message = inputField.value.trim();
    if (message === '') return;

    addMessage(message, 'user');
    inputField.value = '';

    const loadingMessageId = addLoadingIndicator();

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ message })
        });
        const data = await response.json();

        removeLoadingIndicator(loadingMessageId);

        addMessage(data.response, 'model');
    } catch (error) {
        console.error('Ошибка:', error);
        removeLoadingIndicator(loadingMessageId);
        addMessage('Ошибка при получении ответа от сервера', 'model');
    }
});

document.getElementById('clear-chat').addEventListener('click', () => {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';
});

function addMessage(text, sender) {
    const chatBox = document.getElementById('chat-box');
    const messageElem = document.createElement('div');
    messageElem.classList.add('chat-message', sender);

    const timestamp = new Date().toLocaleTimeString();
    messageElem.innerHTML = `<span class="message-text">${text}</span><span class="timestamp">${timestamp}</span>`;

    chatBox.appendChild(messageElem);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addLoadingIndicator() {
    const chatBox = document.getElementById('chat-box');
    const loadingElem = document.createElement('div');
    loadingElem.classList.add('chat-message', 'model');
    loadingElem.id = 'loading-indicator';
    loadingElem.innerHTML = `<span class="message-text">Модель печатает...</span><span class="timestamp">${new Date().toLocaleTimeString()}</span>`;

    chatBox.appendChild(loadingElem);
    chatBox.scrollTop = chatBox.scrollHeight;
    return loadingElem.id;
}

function removeLoadingIndicator(id) {
    const elem = document.getElementById(id);
    if (elem) {
        elem.remove();
    }
}
