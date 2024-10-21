document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("mashup-form");
    const statusMessage = document.getElementById("status-message");

    form.addEventListener("submit", function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Show a loading message
        statusMessage.textContent = "Generating mashup... Please wait.";
        statusMessage.style.color = "blue";

        // Submit the form using AJAX or fetch
        const formData = new FormData(form);
        
        fetch(form.action, {
            method: "POST",
            body: formData
        })
        .then(response => {
            if (response.ok) {
                return response.json();
            } else {
                throw new Error("Network response was not ok.");
            }
        })
        .then(data => {
            // Show success message
            statusMessage.textContent = data.message;
            statusMessage.style.color = "green";
        })
        .catch(error => {
            console.error("There was a problem with the fetch operation:", error);
            statusMessage.textContent = "Error generating mashup. Please try again.";
            statusMessage.style.color = "red";
        });
    });
});
