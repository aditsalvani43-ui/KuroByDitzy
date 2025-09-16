const chatbox = document.getElementById('chatbox');
const userInput = document.getElementById('userInput');
const sendBtn = document.getElementById('sendBtn');

function addMessage(sender, text) {
    const div = document.createElement('div');
    div.className = 'message';
    div.innerHTML = `<strong>${sender}:</strong> ${text}`;
    chatbox.appendChild(div);
    chatbox.scrollTop = chatbox.scrollHeight;
}

sendBtn.onclick = async () => {
    const message = userInput.value.trim();
    if (!message) return;
    addMessage('Kamu', message);
    userInput.value = '';
    // Kirim ke backend
    try {
        const res = await fetch('/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({message})
        });
        const data = await res.json();
        addMessage('AI', data.reply);
    } catch (e) {
        addMessage('AI', 'Gagal mendapatkan jawaban.');
    }
};

userInput.addEventListener("keyup", function(e) {
    if (e.key === "Enter") sendBtn.onclick();
});
