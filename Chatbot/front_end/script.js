document.addEventListener("DOMContentLoaded", () => {
    const chatBox = document.getElementById("chat-box");
    const userInput = document.getElementById("user-input");
    const sendButton = document.getElementById("send-button");

    // Append message to chat box
    const appendMessage = (message, isUser) => {
        const messageElement = document.createElement("div");
        messageElement.classList.add("message", isUser ? "user-message" : "bot-message");
        messageElement.textContent = message;
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Send message to Rasa server
    const sendMessage = async (message) => {
        if (!message.trim()) return;

        // Append user's message to chat
        appendMessage(message, true);

        // Clear the input field
        userInput.value = "";

        // Send request to Rasa backend
        try {
            const response = await fetch("http://localhost:5005/webhooks/rest/webhook", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ sender: "user", message: message }),
            });

            const data = await response.json();
            if (data.length) {
                data.forEach((res) => appendMessage(res.text, false));
            } else {
                appendMessage("I'm sorry, I didn't understand that.", false);
            }
        } catch (error) {
            appendMessage("Error connecting to the server. Please try again later.", false);
        }
    };

    // Handle send button click
    sendButton.addEventListener("click", () => {
        const message = userInput.value;
        sendMessage(message);
    });

    // Handle Enter key press
    userInput.addEventListener("keypress", (event) => {
        if (event.key === "Enter") {
            const message = userInput.value;
            sendMessage(message);
        }
    });
});
