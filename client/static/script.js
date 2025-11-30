
const DEFAULT_BG = '../static/image/background_pic1.png';
const savedBg     = localStorage.getItem('siteBg');
document.body.style.background =
    `url('${savedBg || DEFAULT_BG}') center/cover fixed`;

const bar   = document.getElementById('timerBar');
const cdTxt = document.getElementById('countDownTxt');
const target = new Date('2026-01-01T00:00:00+03:00');


const galPopup = document.getElementById('galPopup');
const thumbs   = [...document.querySelectorAll('.thumb')];
const popup    = document.getElementById('galPopup');
const bigImg   = document.getElementById('bigImg');
const prevBtn  = document.getElementById('prevBtn');
const nextBtn  = document.getElementById('nextBtn');

const formPop = document.getElementById('formPopup');
const openBtn = document.getElementById('openFormBtn');
const closeBtn = document.getElementById('formClose');
const feedForm = document.getElementById('feedForm');
const sendBtn  = document.getElementById('sendBtn');



document.getElementById('galClose').addEventListener('click', closePop);

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



function updateTimer(){
    const diff = target - Date.now();
    if(diff<=0){ cdTxt.textContent='🎉 Новый год уже сегодня!'; return; }
    const d=Math.floor(diff/864e5),
        h=Math.floor(diff/36e5)%24,
        m=Math.floor(diff/6e4)%60,
        s=Math.floor(diff/1e3)%60;
    cdTxt.textContent =
        `До нового года: ${d}д ${h}ч ${m}м ${s}с`;
    requestAnimationFrame(updateTimer);
}
updateTimer();


const chatBox = document.querySelector('.chat-container');
const GAP     = 20;
const TOP_GAP =  0;

function placeTimer(){

    const rawLeft = chatBox.offsetLeft + chatBox.offsetWidth + GAP;
    const rawTop  = chatBox.offsetTop + TOP_GAP;
    bar.style.left = rawLeft + 'px';
    bar.style.top  = rawTop  + 'px';
    bar.dataset.startY = rawTop;
}

window.addEventListener('resize', placeTimer);
placeTimer();

window.addEventListener('scroll', () => {
    const fixedNow = window.scrollY >= +bar.dataset.startY;

    if (fixedNow) {
        if (!bar.classList.contains('fixed')) {
            bar.classList.add('fixed');
            bar.style.top = '10px';
        }
    } else {
        if (bar.classList.contains('fixed')) {
            bar.classList.remove('fixed');
            placeTimer();
        }
    }


    if (bar.classList.contains('fixed')) {
        const rawLeft = chatBox.offsetLeft + chatBox.offsetWidth + GAP;
        bar.style.left = rawLeft + 'px';
    }
});



let cur = 0;

thumbs.forEach((t, i) => t.addEventListener('click', () => openPop(i)));

prevBtn.onclick = () => openPop(cur - 1);
nextBtn.onclick = () => openPop(cur + 1);

function openPop(i) {
    cur = i;
    showImg();
    galPopup.classList.add('show');
}

function closePop() {
    galPopup.classList.remove('show');
    document.body.style.background = `url('${thumbs[cur].src}') center/cover fixed`;
    localStorage.setItem('siteBg', thumbs[cur].src);
}

function showImg(){
    bigImg.src = thumbs[cur].src;
    prevBtn.disabled = cur===0;
    nextBtn.disabled = cur===thumbs.length-1;
}



function resetForm() {
    feedForm.reset();
    sendBtn.classList.remove('sending', 'done');
    sendBtn.textContent = 'Отправить';
    sendBtn.disabled = false;
}


openBtn.addEventListener('click', () => {
    resetForm();
    formPop.classList.add('show');
});

closeBtn.addEventListener('click', () => formPop.classList.remove('show'));


feedForm.addEventListener('submit', async e => {
    e.preventDefault();

    const tel  = feedForm.tel.value.trim();
    const mail = feedForm.mail.value.trim();
    const txt  = feedForm.text.value.trim();


    const okTel  = /^\+?\d{10,15}$/.test(tel);
    const okMail = /^[\w.-]+@[\w.-]+\.\w{2,}$/.test(mail);
    const okTxt  = /^[A-Za-zА-Яа-яЁё0-9\s.,!?]+$/.test(txt);

    if (!(okTel)) {
        alert('Проверьте ввод: телефон');
        return;
    }

    if (!(okMail)) {
        alert('Проверьте ввод: e-mail');
        return;
    }
    if (!(okTxt)) {
        alert('Проверьте ввод: текст (только RU/EN и цифры).');
        return;
    }


    sendBtn.classList.add('sending');

    sendBtn.textContent = 'Отправляем…';
    sendBtn.disabled = true;
    await new Promise(resolve => setTimeout(resolve, 50));
    try {
        await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tel, mail, txt })
        });
        await new Promise(resolve => setTimeout(resolve, 500));

        sendBtn.classList.remove('sending');

        sendBtn.classList.add('done');
        sendBtn.textContent = 'Успешно отправлено';
    } catch (err) {
        alert('Ошибка отправки, попробуйте позже.');
        sendBtn.classList.remove('sending');
        sendBtn.disabled = false;
        sendBtn.textContent = 'Отправить';
    }
});



const helloPop   = document.getElementById('helloPop');
const helloClose = document.getElementById('helloClose');

if (!localStorage.getItem('helloClosed')) {
    setTimeout(() => helloPop.classList.add('show'), 30_000);
}

helloClose.addEventListener('click', () => {
    helloPop.classList.remove('show');
    localStorage.setItem('helloClosed', '1');
});



const decor = document.getElementById('decor');

window.addEventListener('mousemove', e => {
    decor.style.transform = `rotate(${e.clientX}deg)`;
});

window.addEventListener('scroll', () => {
    const k = 1 + window.scrollY / 1000;
    decor.style.scale = k;
});
