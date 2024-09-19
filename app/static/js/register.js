document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");
    const usernameInput = document.getElementById("text-93a0");
    const emailInput = document.getElementById("text-8d97");
    const passwordInput = document.getElementById("password");
    const confirmPasswordInput = document.getElementById("confirm_password");

    // Event listener for form submission
    form.addEventListener("submit", function (e) {
        e.preventDefault();  // Prevent form submission until validation is complete
        e.stopImmediatePropagation();  // Prevent other submit handlers


        // Disable submit button to prevent multiple submissions
        const submitButton = form.querySelector("input[type='submit']");
        submitButton.disabled = true;

        // Check if passwords match
        if (passwordInput.value !== confirmPasswordInput.value) {
            alert("Passwords do not match. Please try again.");
            submitButton.disabled = false;  // Re-enable the submit button
            return;
        }

        // Perform username and email validation with the server
        validateUser(usernameInput.value, emailInput.value).then((response) => {
            if (response.usernameExists && response.emailExists) {
                alert("Both username and email are already taken. Please use different ones.");
                submitButton.disabled = false;  // Re-enable the submit button
            } else if (response.usernameExists) {
                alert("Username already exists. Please choose another one.");
                submitButton.disabled = false;  // Re-enable the submit button
            } else if (response.emailExists) {
                alert("Email already exists. Please use another one.");
                submitButton.disabled = false;  // Re-enable the submit button
            } else {
                // If no validation errors, submit the form
                form.submit();
            }
        }).catch((error) => {
            console.error("Error during validation: ", error);
            alert("An error occurred during validation. Please try again.");
            submitButton.disabled = false;  // Re-enable the submit button
        });
    });

    // Function to validate username and email with the server
    async function validateUser(username, email) {
        const response = await fetch("/check_user_exists", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ username: username, email: email })
        });

        return response.json();  // Assuming server returns { usernameExists: true/false, emailExists: true/false }
    }
});
