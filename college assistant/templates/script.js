function sendMessage() {
    let userInput = document.getElementById("user-input").value;
    let chatBox = document.getElementById("chat-box");

    if (userInput.trim() === "") return;

    // Display user message
    let userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = userInput;
    chatBox.appendChild(userMessage);

    // Clear input field
    document.getElementById("user-input").value = "";

    // Send message to Rasa server
    fetch("http://localhost:5005/webhooks/rest/webhook", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ sender: "user", message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        data.forEach(msg => {
            let botMessage = document.createElement("div");
            botMessage.className = "bot-message";
            botMessage.textContent = msg.text;
            chatBox.appendChild(botMessage);
        });

        // Auto-scroll to the latest message
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error("Error:", error));
}
