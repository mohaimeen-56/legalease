async function simplifyText() {
    let inputText = document.getElementById("inputText").value;
    let outputText = document.getElementById("outputText");
    let loadingMessage = document.getElementById("loadingMessage");

    if (!inputText.trim()) {
        alert("Please enter a message");
        return;
    }

    loadingMessage.style.display = "block";
    outputText.value = "";

    try {
        let response = await fetch("http://127.0.0.1:8000/simplify", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ text: inputText })
        });

        let data = await response.json();
        console.log(data);

        if (response.ok) {
            outputText.value = data.simplified_text;
        } else {
            alert("Error: " + data.detail);
        }
    } catch (error) {
        console.error("Error:", error);
        alert("An error occurred while processing.");
    } finally {
        loadingMessage.style.display = "none";
    }
}
