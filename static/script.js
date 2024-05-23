document.getElementById('send-button').addEventListener('click', function() {
    const input = document.getElementById('message-input');
    const message = input.value.trim();
    if (!message) return; // Avoid sending empty messages
    displayMessage(message, 'You'); // Display user message right-aligned
    input.value = ''; // Clear input after sending

    // Send the user input to the Flask server and handle the response
    fetch('/get_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: message })
    })
    .then(response => response.json())
    .then(data => {
        displayMessage(data.response, 'Bot'); // Display bot response left-aligned
    })
    .catch(error => console.error('Error:', error));
});

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message-bubble', sender.toLowerCase());
    const icon = document.createElement('img');
    icon.className = 'message-icon';
    icon.alt = 'Icon';
    const textNode = document.createElement('span');
    textNode.textContent = message;
    icon.style.width = '24px';
    icon.style.height = '24px';
    messageElement.style.marginBottom = '5px';
    src = 'https://upload.wikimedia.org/wikipedia/en/2/2e/Indian_Institute_of_Information_Technology%2C_Allahabad_Logo.png';
    src = 'https://as2.ftcdn.net/v2/jpg/00/65/77/27/1000_F_65772719_A1UV5kLi5nCEWI0BNLLiFaBPEkUbv5Fv.jpg';
    if (sender === 'You') {
        messageElement.style.textAlign = 'right';
        messageElement.style.backgroundColor = '#f0f0f0'; // Light theme user message
        icon.src = src; // Path to user icon
        icon.alt = 'User';
        messageElement.appendChild(textNode);
        messageElement.appendChild(icon); // Add icon after text for right alignment
    } else {
        messageElement.style.textAlign = 'left';
        messageElement.style.backgroundColor = '#e0e0e0'; // Light theme bot message
        icon.src = 'https://upload.wikimedia.org/wikipedia/en/2/2e/Indian_Institute_of_Information_Technology%2C_Allahabad_Logo.png'; // Path to bot icon
        icon.alt = 'Bot';
        messageElement.appendChild(icon); // Add icon before text for left alignment
        messageElement.appendChild(textNode);
    }
    document.getElementById('message-container').appendChild(messageElement);
    document.getElementById('message-container').scrollTop = document.getElementById('message-container').scrollHeight;
}