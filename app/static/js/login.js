// static/js/login.js

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("login-form");
    const usernameInput = document.getElementById("username");
    const passwordInput = document.getElementById("password");

    form.addEventListener("submit", function (e) {
        e.preventDefault(); // Prevent default form submission
        e.stopImmediatePropagation();  // Prevent other submit handlers

        // Client-side validation
        const username = usernameInput.value.trim();
        const password = passwordInput.value;

        if (!username || !password) {
            alert("Please enter both username and password.");
            return;
        }

        // Disable submit button to prevent multiple submissions
        const submitButton = form.querySelector("button[type='submit']");
        submitButton.disabled = true;

        // Send AJAX POST request to server
        fetch("/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: username, password: password })
        })
        .then(response => response.json())
        .then(data => {
            submitButton.disabled = false;

            if (data.success) {
                // Redirect to home page or another page upon successful login
                window.location.href = "/home";
            } else {
                alert(data.message || "Login failed. Please try again.");
            }
        })
        .catch(error => {
            console.error("Error during login:", error);
            alert("An error occurred during login. Please try again.");
            submitButton.disabled = false;
        });
    });
});
